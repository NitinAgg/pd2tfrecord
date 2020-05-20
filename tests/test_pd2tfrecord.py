from tempfile import NamedTemporaryFile

import numpy as np
import pandas as pd

from pd2tfrecord import load_tfrecords_to_dataframe, write_to_tfrecords


def test_e2e() -> None:
    test_data_dict = {
        "int_feature": [0, 1, 2],
        "float_feature": [1.1, 2.2, 3.3],
        "str_feature": ["a", "bc", "def"],
    }
    test_df = pd.DataFrame(data=test_data_dict)
    with NamedTemporaryFile() as fp:
        write_to_tfrecords(test_df, fp.name)
        actual_df = load_tfrecords_to_dataframe(fp.name)
        actual_df.str_feature = actual_df.str_feature.str.decode("utf-8")
        print(actual_df)
        print(test_df)
        assert (actual_df.int_feature == test_df.int_feature).all()
        assert (actual_df.str_feature == test_df.str_feature).all()
        assert np.allclose(actual_df.float_feature, test_df.float_feature)
