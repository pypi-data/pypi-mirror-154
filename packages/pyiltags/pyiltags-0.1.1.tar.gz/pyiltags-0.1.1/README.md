# PyILTags

## Description

**PyILTags** is a pure **Python** implementation of the
[InterlockLedger ILTags](https://github.com/interlockledger/specification/tree/master/ILTags)
TLV encoding.

It implements all tags defined by the standard, each one with proper interfaces to manipulate
their data. It can also handle any non standard tag as instances of `ILRawTag`.

Furthermore, the provided API allows the implementation of new tags from ground up or by reusing
one of the existing standard tags with new IDs.

## Requirements

This program was developed for Python 3.7 or higher.

It depends on [PyILInt 0.2.2](https://pypi.org/project/pyilint/) or later to work properly.

## Installation

To install this library, you may download the code from 
[github](https://github.com/interlockledger/pyiltags) and copy
the contents of the directory ``src`` into your module's directory.

You can also use **pip** to install it by running the command:

```
$ pip install pyiltags
```

## How to use it

This library can be used to create, serialize and deserialize values
using the **ILTags** standard.

This is a very simple example about how to use this library to
create, serialize and deserialize a tag:

```python
from io import BytesIO
from pyiltags.standard import ILStandardTagFactory, ILUInt64Tag

# Serialize a tag
tag = ILUInt64Tag(123456)
writer = BytesIO()
tag.serialize(writer)
writer.seek(0)
serialized = writer.read()
print(f'Tag with id {tag.id} and value {tag.value} serialized.')

# Unserialize the tag
reader = BytesIO(serialized)
factory = ILStandardTagFactory()
deserialized_tag = factory.deserialize(reader)
print(
    f'Deserialized tag with id {deserialized_tag.id} and value {deserialized_tag.value}.')
```

Further information about this library can be found in the source code and in
its unit-tests.

## License

This program is licensed under the BSD 3-Clause License.

## Changes

- 0.1.1:
    - Tested on multiple versions of python with tox;
- 0.1.0:
    - Initial public release with minimum functionality;
