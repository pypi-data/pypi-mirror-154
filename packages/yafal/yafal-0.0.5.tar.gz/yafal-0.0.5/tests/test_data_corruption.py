from yafal import YAFALDataset
from yafal.corruption import DatasetCorruptor
import random

random.seed(42)


def _get_corrupted_dataset():
    int_label_dataset = YAFALDataset()
    text_label_dataset = YAFALDataset()
    for i in range(5):
        int_label_dataset.add_sample(
            "Label 1 data", sample_labels=[1]
        )
        int_label_dataset.add_sample(
            "Label 0 data", sample_labels=[0]
        )
        # Text dataset
        text_label_dataset.add_sample(
            "Label 1 data", sample_labels=["Yes"]
        )
        text_label_dataset.add_sample(
            "Label 0 data", sample_labels=["No"]
        )
    return int_label_dataset, text_label_dataset


_get_corrupted_dataset()


def test_no_corruption():
    int_label_dataset, text_label_dataset = _get_corrupted_dataset()
    corruptor = DatasetCorruptor(probability=0)
    int_corrupt = corruptor.transform(int_label_dataset)
    text_corrupt = corruptor.transform(text_label_dataset)
    for sample_1, sample_2 in zip(int_label_dataset, int_corrupt):
        assert sample_1 == sample_2

    for sample_1, sample_2 in zip(text_label_dataset, text_corrupt):
        assert sample_1 == sample_2


def test_keep_original_parameter():
    int_label_dataset, text_label_dataset = _get_corrupted_dataset()
    corruptor = DatasetCorruptor(probability=1.1, keep_original=False)
    int_corrupt = corruptor.transform(int_label_dataset)
    text_corrupt = corruptor.transform(text_label_dataset)
    assert len(int_corrupt.samples) == len(int_label_dataset.samples)
    assert len(text_corrupt.samples) == len(text_label_dataset.samples)

    for sample_1, sample_2 in zip(int_label_dataset, int_corrupt):
        # The labels should be different
        assert sample_1[1] != sample_2[1] and sample_1[2] != sample_2[2]
        # Check that the label types are kept (no string converted to integer or vice-versa)
        assert isinstance(sample_1[1][0], type(sample_2[1][0]))

    for sample_1, sample_2 in zip(text_label_dataset, text_corrupt):
        # The labels should be different
        assert sample_1[1] != sample_2[1] and sample_1[2] != sample_2[2]
        # Check that the label types are kept (no string converted to integer or vice-versa)
        assert isinstance(sample_1[1][0], type(sample_2[1][0]))

    corruptor = DatasetCorruptor(probability=1.1, keep_original=True)
    int_corrupt = corruptor.transform(int_label_dataset)
    text_corrupt = corruptor.transform(text_label_dataset)
    assert len(int_corrupt.samples) == 2*len(int_label_dataset.samples)
    assert len(text_corrupt.samples) == 2*len(text_label_dataset.samples)

    # Check that the original items exists on the corrupted datasets

    assert {str(sample) for sample in int_label_dataset}.issubset({str(corrupted) for corrupted in int_corrupt})
    assert {str(sample) for sample in text_label_dataset}.issubset({str(corrupted) for corrupted in text_corrupt})
