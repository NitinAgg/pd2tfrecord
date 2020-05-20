# pd2tfrecord
Library to convert pandas to tfExample and tfRecord file and vice versa.

# Installation
```
pip install pd2tfrecord
```

# Example
Following code runs through an example of coverting a pandas dataframe to a list of serialized tf.Example, write these to .tfrecord files and then read that back into pandas dataframe.

## Setup
```python
import numpy as np
import pandas as pd

# example dataframe we will use through the example
example_df = pd.DataFrame(data={
    "int_feature": [0, 1, 2],
    "float_feature": [1.1, 2.2, 3.3],
    "str_feature": ["a", "bc", "def"],
})
```

## Pandas to tf.Example

```python
from pd2tfrecord import pandas_to_example_list

tfexamples = pandas_to_example_list(example_df)
tfexamples
```

```
Out:
[b'\nG\n\x14\n\x0bstr_feature\x12\x05\n\x03\n\x01a\n\x19\n\rfloat_feature\x12\x08\x12\x06\n\x04\xcd\xcc\x8c?\n\x14\n\x0bint_feature\x12\x05\x1a\x03\n\x01\x00',
 b'\nH\n\x14\n\x0bint_feature\x12\x05\x1a\x03\n\x01\x01\n\x15\n\x0bstr_feature\x12\x06\n\x04\n\x02bc\n\x19\n\rfloat_feature\x12\x08\x12\x06\n\x04\xcd\xcc\x0c@',
 b'\nI\n\x16\n\x0bstr_feature\x12\x07\n\x05\n\x03def\n\x19\n\rfloat_feature\x12\x08\x12\x06\n\x0433S@\n\x14\n\x0bint_feature\x12\x05\x1a\x03\n\x01\x02']
```

## tf.Example to Pandas
```python
from pd2tfrecord import examples_to_dataframe

examples_to_dataframe(tfexamples)
```

```
Out:
  str_feature  float_feature  int_feature
0        b'a'            1.1            0
1       b'bc'            2.2            1
2      b'def'            3.3            2
```
Notice how str_features are now encoded, this is because tf.Example only supports encoded strings. It is recommended that the input dataframe has only encoded string columns to avoid errors.


## Pandas to .tfrecord
This will write out the dataframe to a tfrecord file, which is essentially a serialized tf.Example per row of the file.

```python
from pd2tfrecord import write_to_tfrecords

write_to_tfrecords(example_df, filename="example.tfrecord")
```

## .tfrecord to pandas 
```python
from pd2tfrecord import load_tfrecords_to_dataframe

load_tfrecords_to_dataframe("example.tfrecord")
```

```
  str_feature  float_feature  int_feature
0        b'a'            1.1            0
1       b'bc'            2.2            1
2      b'def'            3.3            2
```
Notice how str_features are now encoded, this is because tf.Example only supports encoded strings. It is recommended that the input dataframe has only encoded string columns to avoid errors.
