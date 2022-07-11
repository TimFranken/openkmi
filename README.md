# OpenKMI

Python package to download open data (observations and forecasts) from KMI.

```python
# example to get the windspeed for Stabroek starting from 2021 - present
from openkmi.point_obs import Synop
kmi = Synop()
df = kmi.get_data('6438', start_date='2021-01-01T00:00:00', parameter_list=['wind_speed'])
```

## Description

OpenKMI serves as a simple wrapper around the open data that the Royal Meteorological Institute of Belgium (RMI)
offers. At present following data is implemented:
* Synoptic observations
* Automatic weather stations (AWS)
* ALARO forecasts

The package facilitates fetching data from the existing WFS and WMS services to download this data.

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

### ALARO

The weather model 'Alaro' is a numerical forecast model that simulates the evolution of the atmosphere.
The scientists of the RMI attempt constantly to improve these models on the basis of these newest numerical techniques,
the parameterisation of physical processes and the use of meteorological observations.

The results of this research are processed in the operational weather model ALARO. It is used by the weather
forecasters of the weather office, and for creating products and services for the general public.

All the parameters of the last run of Alaro can be downloaded.
This data is generated automatically from ALARO every six hours.
**They aren't corrected or interpreted by the forecasters of the RMI.**
A correct interpretation of this data requires some expertise.

We refer to the [metadata](https://opendata.meteo.be/geonetwork/srv/eng/catalog.search;jsessionid=1A4FC7644B7C0B8D17287BA7A9A21278#/metadata/RMI_DATASET_ALARO)
for more information.

## Installation

```
pip install openkmi
```

## Examples

See the notebooks under examples to get you started.

### Quick start:

#### Point observations
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

#### Alaro model forecasts

```python
from openkmi.grid_data import Alaro

# initialise synoptic data
kmi = Alaro()

# get the available layers (parameters)
parameters = kmi.get_parameters()

# get more information on a layer
abstract = kmi.get_parameter_info('2_m_temperature')

# get available forecasting times
idx = kmi.get_times('2_m_temperature')

# get the data for a certain location (coordinates in WGS84)
df = kmi.get_data('2_m_temperature', 4.6824, 52.3617)

# get the data for a certain location (in Lambert72)
df = kmi.get_data('2_m_temperature', 169955, 338336, epsg='31370')
```