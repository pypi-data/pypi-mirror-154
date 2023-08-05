#!/usr/bin/env python3
"""
Pre-processing pipeline for NSynth pitch detection
"""

import logging
from functools import partial
from pathlib import Path
from typing import Any, Dict

import luigi
import pandas as pd

import hearpreprocess.pipeline as pipeline
from hearpreprocess.pipeline import (
    TEST_PERCENTAGE,
    TRAIN_PERCENTAGE,
    TRAINVAL_PERCENTAGE,
    VALIDATION_PERCENTAGE,
)

logger = logging.getLogger("luigi-interface")


generic_task_config: Dict[str, Any] = {
    "task_name": "nsynth_pitch",
    "version": "v2.2.3",
    "embedding_type": "scene",
    "prediction_type": "multiclass",
    "split_mode": "trainvaltest",
    "sample_duration": 4.0,
    "pitch_range_min": 21,
    "pitch_range_max": 108,
    "evaluation": ["pitch_acc", "chroma_acc"],
    "download_urls": [
        {
            "split": "train",
            "url": "http://download.magenta.tensorflow.org/datasets/nsynth/nsynth-train.jsonwav.tar.gz",  # noqa: E501
            "md5": "fde6665a93865503ba598b9fac388660",
        },
        {
            "split": "valid",
            "url": "http://download.magenta.tensorflow.org/datasets/nsynth/nsynth-valid.jsonwav.tar.gz",  # noqa: E501
            "md5": "87e94a00a19b6dbc99cf6d4c0c0cae87",
        },
        {
            "split": "test",
            "url": "http://download.magenta.tensorflow.org/datasets/nsynth/nsynth-test.jsonwav.tar.gz",  # noqa: E501
            "md5": "5e6f8719bf7e16ad0a00d518b78af77d",
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
                "test": 3600 * 5 * TEST_PERCENTAGE / TRAINVAL_PERCENTAGE,
            }
        },
        "50h": {
            "max_task_duration_by_split": {
                "train": 3600 * 50 * TRAIN_PERCENTAGE / TRAINVAL_PERCENTAGE,
                "valid": 3600 * 50 * VALIDATION_PERCENTAGE / TRAINVAL_PERCENTAGE,
                "test": 3600 * 50 * TEST_PERCENTAGE / TRAINVAL_PERCENTAGE,
            }
        },
        "small": {
            "download_urls": [
                {
                    "split": "train",
                    "url": "https://github.com/hearbenchmark/hear2021-open-tasks-downsampled/raw/main/nsynth-train-small.zip",  # noqa: E501
                    "md5": "c17070e4798655d8bea1231506479ba8",
                },
                {
                    "split": "valid",
                    "url": "https://github.com/hearbenchmark/hear2021-open-tasks-downsampled/raw/main/nsynth-valid-small.zip",  # noqa: E501
                    "md5": "e36722262497977f6b945bb06ab0969d",
                },
                {
                    "split": "test",
                    "url": "https://github.com/hearbenchmark/hear2021-open-tasks-downsampled/raw/main/nsynth-test-small.zip",  # noqa: E501
                    "md5": "9a98e869ed4add8ba9ebb0d7c22becca",
                },
            ],
            "max_task_duration_by_split": {"train": None, "valid": None, "test": None},
        },
    },
}


class ExtractMetadata(pipeline.ExtractMetadata):
    train = luigi.TaskParameter()
    test = luigi.TaskParameter()
    valid = luigi.TaskParameter()

    def requires(self):
        return {
            "train": self.train,
            "test": self.test,
            "valid": self.valid,
        }

    @staticmethod
    def get_rel_path(root: Path, item: pd.DataFrame) -> Path:
        # Creates the relative path to an audio file given the note_str
        audio_path = root.joinpath("audio")
        filename = f"{item}.wav"
        return audio_path.joinpath(filename)

    @staticmethod
    def get_split_key(df: pd.DataFrame) -> pd.Series:
        """
        The instrument is the split key.
        """
        return df["unique_filestem"].apply(lambda filename: filename.split("-")[0])

    def get_requires_metadata(self, split: str) -> pd.DataFrame:
        logger.info(f"Preparing metadata for {split}")

        # Loads and prepares the metadata for a specific split
        split_path = Path(self.requires()[split].workdir).joinpath(split)
        split_path = split_path.joinpath(f"nsynth-{split}")

        metadata = pd.read_json(split_path.joinpath("examples.json"), orient="index")

        metadata = (
            # Filter out pitches that are not within the range
            metadata.loc[
                metadata["pitch"].between(
                    self.task_config["pitch_range_min"],
                    self.task_config["pitch_range_max"],
                )
                # Assign metadata columns
            ].assign(
                relpath=lambda df: df["note_str"].apply(
                    partial(self.get_rel_path, split_path)
                ),
                label=lambda df: df["pitch"],
                split=lambda df: split,
            )
        )

        return metadata


def extract_metadata_task(task_config: Dict[str, Any]) -> pipeline.ExtractMetadata:
    # Build the dataset pipeline with the custom metadata configuration task
    download_tasks = pipeline.get_download_and_extract_tasks(task_config)

    return ExtractMetadata(
        outfile="process_metadata.csv", task_config=task_config, **download_tasks
    )
