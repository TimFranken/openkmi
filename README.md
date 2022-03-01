# OpenKMI

Python package to download open data from KMI.

## Description

OpenKMI serves as a simple wrapper around the open data that the Royal Meteorological Institute of Belgium (RMI)
offers. At present data from the Synoptic observations and the Automatic weather stations (AWS) are implemented.
The package facilitates fetching data from the existing WFS services to download this data.

This is not an official package from the RMI.

### Synoptic observations

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

### Automatic weather stations

RMI operates a network of 17 automatic weather stations in Belgium. These weather stations report meteorological
parameters such as air pressure, temperature, relative humidity, precipitation (quantity, duration),
wind (speed, gust, direction), sunshine duration, shortwave solar radiation and infrared radiation every 10 minutes.
Hourly and daily AWS data are computed from the 10-min observations.

At present only the data for station 'Zeebrugge' and 'Humain' from 2017-11-18 onwards are publicly available.


## Installation

```
pip install openkmi
```

## Examples

See the notebooks under examples to get you started.

### Quick start:


```python
from openkmi.point_obs import Synop
from openkmi.point_obs import AWS

# initialise synoptic data
kmi = Synop()

# initialise AWS data
# default is hourly
kmi_aws_hour = AWS()
# 10-min data:
kmi_aws_10min = AWS(freq='10T')
# Daily data:
kmi_aws_day = AWS(freq='D')

# get the available stations
df_stations = kmi.get_stations()

# get the available parameters
params = kmi.get_parameters()

# example to get the windspeed for a station starting from 2021 - present
df = kmi.get_data('6438', start_date='2021-01-01T00:00:00', parameter_list=['wind_speed'])

# Use more advanced filtering methods
from owslib.fes import PropertyIsEqualTo
custom_filt = PropertyIsEqualTo(propertyname='precip_range', literal='2')
df_r = kmi.get_data('6447', start_date='2020-01-01T00:00:00', end_date='2021-01-01T00:00:00',
                    parameter_list=['precip_quantity', 'precip_range'], custom_filter=custom_filt)
```