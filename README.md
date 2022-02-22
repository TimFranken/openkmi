# pyRMI

pyRMI serves as a wrapper around the WFS service that the Royal Meteorological Institute of Belgium (RMI) offers to download the synoptic measurements.

This is not an official RMI package.

Check the [metadata](https://opendata.meteo.be/geonetwork/srv/eng/catalog.search;jsessionid=A7FEA3AF21132DE8B1DA8A2CD1746597#/metadata/RMI_DATASET_SYNOP) 
and [documentation](https://opendata.meteo.be/documentation/?dataset=synop)
of the synoptic measurements for more info.

## Getting started

See the notebook under examples to get you started.

Quik start:

```python
from pyrmi.synoptic import Synop

# initialise
kmi = Synop()

# get the available stations
df_stations = kmi.get_stations()

# get the available parameters
params = kmi.get_parameters()

# example to get the windspeed for a station starting from 2021 - present
df = kmi.get_data('6438', start_date='2021-01-01T00:00:00', parameter_list=['wind_speed'])
```