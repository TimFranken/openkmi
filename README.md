# OpenKMI

Python package to download open data from KMI.

## Description

OpenKMI serves as a wrapper around the open data that the Royal Meteorological Institute of Belgium (RMI)
offers. At present only the Synoptic observations are implemented. The package serves as a wrapper around the existing
WFS service to download the SYNOP data.

The SYNOP data of RMI contain the observations of the synoptic network (22 stations) for the following parameters:
1. Precipitation: PRECIP_QUANTITY + PRECIP_RANGE
2. Temperature: TEMP + TEMP_MIN + TEMP_MAX + TEMP_GRASS_MIN
3. Wind: WIND_SPEED + WIND_SPEED_UNIT + WIND_DIRECTION + WIND_PEAK_SPEED
4. relative humidity: HUMIDITY_RELATIVE
5. weather type: current weather
6. air pressure: PRESSURE of PRESSURE_STATION_LEVEL
7. sunshine duration: SUN_DURATION_24H
8. Global radiation: SHORT_WAVE_FROM_SKY_24HOUR
9. Total cloudiness: CLOUDINESS

We refer to the [metadata](https://opendata.meteo.be/geonetwork/srv/eng/catalog.search;jsessionid=A7FEA3AF21132DE8B1DA8A2CD1746597#/metadata/RMI_DATASET_SYNOP) 
and [documentation](https://opendata.meteo.be/documentation/?dataset=synop)
of the synoptic measurements for more info.

This is not an official package from the RMI.


## Installation

```
pip install openkmi
```

## Examples

See the notebook under examples to get you started.

Quick start:

```python
from openkmi.synoptic import Synop

# initialise
kmi = Synop()

# get the available stations
df_stations = kmi.get_stations()

# get the available parameters
params = kmi.get_parameters()

# example to get the windspeed for a station starting from 2021 - present
df = kmi.get_data('6438', start_date='2021-01-01T00:00:00', parameter_list=['wind_speed'])
```