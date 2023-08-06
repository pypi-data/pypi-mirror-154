import copy
import os

from yafal import YAFALDataset, YAFALRegression
from yafal.corruption import DatasetCorruptor
from yafal.exceptions import InvalidMethodException, DescriptorsRequiredException

train_yafal_dataset = YAFALDataset()
for i in range(50):
    train_yafal_dataset.add_sample(
        text="Marvin is a happy robot",
        sample_labels=[0]
    )
    train_yafal_dataset.add_sample(
        text="The ultimate answer is 42",
        sample_labels=[1]
    )

test_yafal_dataset = copy.deepcopy(train_yafal_dataset)

semantic_yafal_dataset = YAFALDataset()
for i in range(50):
    semantic_yafal_dataset.add_sample(
        text="Marvin is a happy robot",
        sample_labels=["robot"]
    )
    semantic_yafal_dataset.add_sample(
        text="The ultimate answer is 42",
        sample_labels=["life"]
    )

semantic_test_dataset = copy.deepcopy(semantic_yafal_dataset)


def test_train_binary_model():
    # Train our model
    yafal_regression = YAFALRegression(label_encoder_method="binary", verbose=True, max_epochs=5,
                                       mlp_layer_sizes=(150, 75))
    yafal_regression.fit(train_yafal_dataset)
    # Corrupt the dataset
    corruptor = DatasetCorruptor()
    corrupted_test_dataset = corruptor.transform(test_yafal_dataset)

    # Predict with our model
    for sample, labels, is_corrupted in corrupted_test_dataset:
        _ = yafal_regression.predict([sample], labels=labels)

    yafal_regression.save("test.pck")
    os.remove("test.pck")


def test_train_semantic_model():
    # Train our model
    yafal_regression = YAFALRegression(label_encoder_method="semantic", verbose=True, max_epochs=5,
                                       mlp_layer_sizes=(150, 75))
    yafal_regression.fit(semantic_yafal_dataset, descriptors={"robot": ["Marvin"],
                                                              "life": ["meaning of life"]})

    # Corrupt the dataset
    corruptor = DatasetCorruptor()
    corrupted_test_dataset = corruptor.transform(semantic_test_dataset)

    # Predict with our model
    for sample, labels, is_corrupted in corrupted_test_dataset:
        _ = yafal_regression.predict([sample], labels=labels)


def test_trigger_no_description_exceptions():
    try:
        YAFALRegression(label_encoder_method="potatoes", verbose=True, max_epochs=5)
        raise Exception
    except InvalidMethodException:
        pass

    try:
        yafal_regression = YAFALRegression(label_encoder_method="semantic", verbose=True, max_epochs=5)
        yafal_regression.fit(semantic_yafal_dataset, descriptors={"robot": ["Marvin"]})
        raise Exception
    except DescriptorsRequiredException:
        pass

    try:
        yafal_regression = YAFALRegression(label_encoder_method="semantic", verbose=True, max_epochs=5)
        yafal_regression.fit(semantic_yafal_dataset)
        raise Exception
    except DescriptorsRequiredException:
        pass
