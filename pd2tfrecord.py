from typing import Any, Callable, Dict, Union

import numpy as np
import pandas as pd
import tensorflow as tf


# The following functions can be used to convert a value to a type compatible
# with tf.Example.
def _bytes_feature(value: Union[str, bytes]) -> tf.train.Feature:
    """Returns a bytes_list from a string / byte."""
    if isinstance(value, type(tf.constant(0))):
        value = value.numpy()  # BytesList won't unpack a string from an EagerTensor.
    if isinstance(value, str):
        value = value.encode("utf-8")
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def _float_feature(value: float) -> tf.train.Feature:
    """Returns a float_list from a float / double."""
    return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))


def _int64_feature(value: int) -> tf.train.Feature:
    """Returns an int64_list from a bool / enum / int / uint."""
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


numpy_type_to_feature_converter: Dict[np.dtype, Callable[[Any], tf.train.Feature]] = {
    np.dtype("int64"): _int64_feature,
    np.dtype("float64"): _float_feature,
    np.dtype("object"): _bytes_feature,
}


def pandas_to_example_list(df: pd.DataFrame) -> list:
    return list(df.apply(lambda r: _row_to_example(r, df.dtypes), axis=1))


def examples_to_dataframe(examples: list) -> pd.DataFrame:
    return pd.DataFrame(list(map(example_to_dict, examples)))


def write_to_tfrecords(df: pd.DataFrame, filename: str) -> None:
    examples = pandas_to_example_list(df)
    with tf.io.TFRecordWriter(filename) as writer:
        for e in examples:
            writer.write(e)


def load_tfrecords_to_dataframe(filenames: Union[str, list]) -> pd.DataFrame:
    if isinstance(filenames, str):
        filenames = [filenames]
    raw_dataset = tf.data.TFRecordDataset(filenames)
    examples = list(raw_dataset.as_numpy_iterator())
    return examples_to_dataframe(examples)


def example_to_dict(serialized_example: bytes) -> dict:
    example = tf.train.Example()
    example.ParseFromString(serialized_example)
    py_dict = {}
    for column, value in example.features.feature.items():
        if value.HasField("float_list"):
            if len(value.float_list.value) > 1:
                raise Exception("Currently our library does not handle list fields")
            py_dict[column] = value.float_list.value[0]
        if value.HasField("int64_list"):
            if len(value.int64_list.value) > 1:
                raise Exception("Currently our library does not handle list fields")
            py_dict[column] = value.int64_list.value[0]
        if value.HasField("bytes_list"):
            if len(value.bytes_list.value) > 1:
                raise Exception("Currently our library does not handle list fields")
            py_dict[column] = value.bytes_list.value[0]
    return py_dict


def _row_to_example(row: dict, column_types: dict) -> bytes:
    feature = {}
    for column, ctype in column_types.items():
        if column in row:
            value = numpy_type_to_feature_converter[ctype](row[column])
            feature[column] = value
    return tf.train.Example(
        features=tf.train.Features(feature=feature)
    ).SerializeToString()
