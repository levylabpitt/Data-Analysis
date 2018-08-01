#from 5.1 "Overview of the Exdir API in Python"

import exdir
import numpy as np

f = exdir.File("mytestfile.exdir")
dset = f.create_dataset("my_data", (100,), dtype="i")
print(dset.shape)
print(dset.dtype)
dset[...] = np.arange(100)
print(dset[0])
print(dset[10])
print(dset[0:100:10])

#create dataset from data directly
dset2 = f.create_dataset("my_data2", data=np.arange(100))
print(dset2[0:100:10])

print(dset[dset[:] > 90])

#create an exdir group
grp = f.create_group("subgroup")

#create dataset within that group
dset3 = grp.create_dataset("another_dataset", (50,), dtype="f")
#python dictionary functionality
dset3 = f["subgroup/another_dataset"]

print(dset3.name)

#iterate through a file to get names
for name in f:
	print(name)
	
#test containership
print("my_data" in f)
print("other_data" in f)

#SETTING ATTRIBUTES
dset.attrs["temperature"] = 99.5
print(dset.attrs["temperature"])
print('temperature' in dset.attrs)

#can have a dictionary as an attribute, NICE
dset.attrs["my_attribute"] = {"key1":"value1", "key2":"value2"}
print(dset.attrs.items())

