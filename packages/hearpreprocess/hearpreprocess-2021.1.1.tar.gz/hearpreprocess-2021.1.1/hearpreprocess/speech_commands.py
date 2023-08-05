#!/usr/bin/env python3
"""
Pre-processing pipeline for Google speech_commands
"""

import os
import re
from pathlib import Path
from typing import Any, Dict

import luigi
import pandas as pd
import soundfile as sf
from tqdm import tqdm

import hearpreprocess.pipeline as pipeline
import hearpreprocess.util.luigi as luigi_util
from hearpreprocess.pipeline import (
    TRAIN_PERCENTAGE,
    TRAINVAL_PERCENTAGE,
    VALIDATION_PERCENTAGE,
)

WORDS = ["down", "go", "left", "no", "off", "on", "right", "stop", "up", "yes"]
BACKGROUND_NOISE = "_background_noise_"
UNKNOWN = "_unknown_"
SILENCE = "_silence_"

generic_task_config = {
    "task_name": "speech_commands",
    "version": "v0.0.2",
    "embedding_type": "scene",
    "prediction_type": "multiclass",
    "split_mode": "trainvaltest",
    "sample_duration": 1.0,
    "evaluation": ["top1_acc"],
    "download_urls": [
        {
            "split": "train",
            "url": "http://download.tensorflow.org/data/speech_commands_v0.02.tar.gz",  # noqa: E501
            "md5": "6b74f3901214cb2c2934e98196829835",
        },
        {
            "split": "test",
            "url": "http://download.tensorflow.org/data/speech_commands_test_set_v0.02.tar.gz",  # noqa: E501
            "md5": "854c580ee90bff80c516491c84544e32",
        },
    ],
    "default_mode": "5h",
    # Different modes for preprocessing this dataset
    # We use all modes EXCEPT small, unless flag "--small" used.
    "modes": {
        "5h": {
            # No more than 5 hours of audio (training + validation)
            "max_task_duration_by_split": {
                "train": 3600 * 5 * TRAIN_PERCENTAGE / TRAINVAL_PERCENTAGE,
                "valid": 3600 * 5 * VALIDATION_PERCENTAGE / TRAINVAL_PERCENTAGE,
                # The test set is 1.33 hours, so we use the entire thing
                "test": None,
            }
        },
        "full": {
            "max_task_duration_by_split": {"test": None, "train": None, "valid": None}
        },
        "small": {
            "download_urls": [
                {
                    "split": "train",
                    "url": "https://github.com/hearbenchmark/hear2021-open-tasks-downsampled/raw/main/speech_commands_v0.02-small.zip",  # noqa: E501
                    "md5": "455123a88b8410d1f955c77ad331524f",
                },
                {
                    "split": "test",
                    "url": "https://github.com/hearbenchmark/hear2021-open-tasks-downsampled/raw/main/speech_commands_test_set_v0.02-small.zip",  # noqa: E501
                    "md5": "26d08374a7abd13ca2f4a4b8424f41d0",
                },
            ],
            "max_task_duration_by_split": {"train": None, "valid": None, "test": None},
        },
    },
}


class GenerateTrainDataset(luigi_util.WorkTask):
    """
    Silence / background samples in the train (and, after split,
    validation) sets need to be created by slicing up longer
    background samples into 1 sec slices.  This is the same method
    used in the TensorFlow dataset generator.
    https://github.com/tensorflow/datasets/blob/79d56e662a15cd11e1fb3b679e0f978c8041566f/tensorflow_datasets/audio/speech_commands.py#L142 # noqa
    """

    # Requires an extracted dataset task to be completed
    train_data = luigi.TaskParameter()

    def requires(self):
        return {"train": self.train_data}

    @property
    def output_path(self):
        return self.workdir

    def run(self):
        train_path = Path(self.requires()["train"].workdir).joinpath("train")
        background_audio = list(train_path.glob(f"{BACKGROUND_NOISE}/*.wav"))
        assert len(background_audio) > 0

        # Read all the background audio files and split into 1 second segments,
        # save all the segments into a folder called _silence_
        silence_dir = os.path.join(self.workdir, SILENCE)
        os.makedirs(silence_dir, exist_ok=True)

        print("Generating silence files from background sounds ...")
        for audio_path in tqdm(background_audio):
            audio, sr = sf.read(str(audio_path))
            assert audio.ndim == 1

            basename = os.path.basename(audio_path)
            name, ext = os.path.splitext(basename)

            for start in range(0, len(audio) - sr, sr // 2):
                audio_segment = audio[start : start + sr]
                filename = f"{name}-{start}{ext}"
                filename = os.path.join(silence_dir, filename)
                sf.write(filename, audio_segment, sr)

        # We'll also create symlinks for the dataset here too to make the next
        # stage of splitting into training and validation files easier.
        for file_obj in train_path.iterdir():
            if file_obj.is_dir() and file_obj.name != BACKGROUND_NOISE:
                linked_folder = Path(os.path.join(self.workdir, file_obj.name))
                assert not linked_folder.exists()
                linked_folder.symlink_to(file_obj.absolute(), target_is_directory=True)

            # Also need the testing and validation splits
            if file_obj.name in ["testing_list.txt", "validation_list.txt"]:
                linked_file = Path(os.path.join(self.workdir, file_obj.name))
                assert not linked_file.exists()
                linked_file.symlink_to(file_obj.absolute())

        self.mark_complete()


class ExtractMetadata(pipeline.ExtractMetadata):
    train = luigi.TaskParameter()
    test = luigi.TaskParameter()

    def requires(self):
        return {
            "train": self.train,
            "test": self.test,
        }

    @staticmethod
    def relpath_to_unique_filestem(relpath: str) -> str:
        """
        Include the label (parent directory) in the filestem.
        """
        # Get the parent directory (label) and the filename
        name = "_".join(Path(relpath).parts[-2:])
        # Remove the suffix
        name = os.path.splitext(name)[0]
        return str(name)

    @staticmethod
    def speaker_hash(unique_filestem: str) -> str:
        """Get the speaker hash as the Split key for speech_commands"""
        hsh = re.sub(r"_nohash_.*$", "", unique_filestem)
        return hsh

    @staticmethod
    def get_split_key(df: pd.DataFrame) -> pd.Series:
        """Get the speaker hash as the split key for speech_commands"""
        return df["unique_filestem"].apply(ExtractMetadata.speaker_hash)

    @staticmethod
    def relpath_to_label(relpath: Path):
        label = os.path.basename(os.path.dirname(relpath))
        if label not in WORDS and label != SILENCE:
            label = UNKNOWN
        return label

    def get_split_paths(self):
        """
        Splits the dataset into train/valid/test files using the same method as
        described in by the TensorFlow dataset:
        https://www.tensorflow.org/datasets/catalog/speech_commands
        """
        # Test files
        test_path = Path(self.requires()["test"].workdir).joinpath("test")
        test_df = pd.DataFrame(test_path.glob("*/*.wav"), columns=["relpath"]).assign(
            split=lambda df: "test"
        )

        # All silence paths to add to the train and validation
        train_path = Path(self.requires()["train"].workdir)
        all_silence = list(train_path.glob(f"{SILENCE}/*.wav"))

        # Validation files
        with open(os.path.join(train_path, "validation_list.txt"), "r") as fp:
            validation_paths = fp.read().strip().splitlines()
        validation_rel_paths = [os.path.join(train_path, p) for p in validation_paths]

        # There are no silence files marked explicitly for validation. We add all
        # the running_tap.wav samples to the silence class for validation.
        # https://github.com/tensorflow/datasets/blob/e24fe9e6b03053d9b925d299a2246ea167dc85cd/tensorflow_datasets/audio/speech_commands.py#L183
        val_silence = list(train_path.glob(f"{SILENCE}/running_tap*.wav"))
        validation_rel_paths.extend(val_silence)
        validation_df = pd.DataFrame(validation_rel_paths, columns=["relpath"]).assign(
            split=lambda df: "valid"
        )

        # Train-test files.
        with open(os.path.join(train_path, "testing_list.txt"), "r") as fp:
            train_test_paths = fp.read().strip().splitlines()
        audio_paths = [
            str(p.relative_to(train_path)) for p in train_path.glob("[!_]*/*.wav")
        ]

        # The final train set is all the audio files MINUS the files marked as
        # test / validation files in testing_list.txt or validation_list.txt
        train_paths = list(
            set(audio_paths) - set(train_test_paths) - set(validation_paths)
        )
        train_rel_paths = [os.path.join(train_path, p) for p in train_paths]

        # Training silence is all the generated silence / background noise samples
        # minus those marked for validation.
        train_silence = list(set(all_silence) - set(val_silence))
        train_rel_paths.extend(train_silence)
        train_df = pd.DataFrame(train_rel_paths, columns=["relpath"]).assign(
            split=lambda df: "train"
        )
        assert len(train_df.merge(validation_df, on="relpath")) == 0

        return pd.concat([test_df, validation_df, train_df]).reset_index(drop=True)

    def get_all_metadata(self) -> pd.DataFrame:
        metadata = self.get_split_paths()
        metadata = metadata.assign(
            label=lambda df: df["relpath"].apply(self.relpath_to_label),
        )
        return metadata


def extract_metadata_task(task_config: Dict[str, Any]) -> pipeline.ExtractMetadata:
    # Build the dataset pipeline with the custom metadata configuration task
    download_tasks = pipeline.get_download_and_extract_tasks(task_config)

    generate = GenerateTrainDataset(
        train_data=download_tasks["train"], task_config=task_config
    )
    return ExtractMetadata(
        train=generate,
        test=download_tasks["test"],
        outfile="process_metadata.csv",
        task_config=task_config,
    )
