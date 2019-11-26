Description:
================================================================================
Process the binary file produced by Catman DAQ system, containing all the
information of the experiment. This file format is faster and occupy less space
than other format, so it is usefull to read them directly and be able to handle
this information outside the native software.

This code is an adaptation of a matlab source for the same purpose. The link of
the source can be found [here](struct://www.mathworks.com/matlabcentral/fileexchange/6780-catman-file-importer).


Instalation:
================================================================================

For installing just use:

````
    pip install git+https://github.com/oldsphere/CatmanReader.git
````

or clone de repository and 

Usage:
================================================================================
For usage just import the library and create a `CatmanReader` object

```python
from catman import CatmanReader

catman_file = CatmanReader('experiment0.BIN')
```

All the information is stored in the `CatmanReader` object, the most
interesting part is the channels recorded, which are stores in the channel
property.

```python
channels_names = [ch['name'] for ch in catman_file.channels]

time = catman_file.channels[0]['data']
data1 = catman_file.channels[3]['data']

```

The data is stores in a list with the intention of transform it to more usefull
format such as `numpy` arrays. 
