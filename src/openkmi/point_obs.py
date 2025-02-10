from owslib.fes import PropertyIsEqualTo, PropertyIsGreaterThanOrEqualTo, PropertyIsLessThan, And, OgcExpression
from owslib.wfs import WebFeatureService
from owslib.etree import etree
import pandas as pd


class Synop:

    def __init__(self):

        self.wfs = WebFeatureService(url='https://opendata.meteo.be/service/synop/wfs', version='1.1.0')
        self.station_wfs = self.wfs
        self.stations = None
        self.data_layer = 'synop:synop_data'

    def _get_contents(self):
        """
        Get the types we can use in the WFS
        :return: list of types
        """
        return list(self.wfs.contents)

    def get_stations(self):
        """
        Get the list of stations that are available for requesting
        :return: pandas dataframe with the list of all stations
        """
        response = self.station_wfs.getfeature(typename='synop:synop_station', outputFormat='csv')
        df_stations = pd.read_csv(response)
        if 'code' in df_stations.columns:
            df_stations['code'] = df_stations['code'].apply(str)
        else:
            df_stations['code'] = df_stations['FID'].apply(lambda x: x.split('.')[1])
        df_stations.drop(columns=['FID'], inplace=True)
        self.stations = df_stations

        return df_stations

    def get_parameters(self):
        """
        Get parameters that we can request for the stations
        :return: dictionary with the parameters
        """
        return self.wfs.get_schema(self.data_layer)['properties']

    def get_data(self, station_code, start_date=None, end_date=None, parameter_list=None,
                 custom_filter=None):
        """
        Return the data for a station
        :param station_code: station code
        :param start_date: start date for which to request the data (string, format: '2021-01-01T00:00:00')
        :param end_date: end date for which to request the data (string, format: '2021-01-01T00:00:00')
        :param parameter_list: List of parameters
        :param custom_filter: (List of) OgcExpression(s) to be used in filtering the data
        :return pandas dataframe with the requested data
        """

        # Get the station list so we can validate the station_code
        if not isinstance(self.stations, pd.DataFrame):
            self.get_stations()

        # Validate the station_code
        if station_code not in self.stations['code'].values:
            raise Exception('station code not valid. Station code should be any of '
                            f'{",".join(self.stations.code.values.astype("str"))}')

        # Start building the filter list
        # First check if we have a custom filter defined
        if isinstance(custom_filter, OgcExpression):
            filter_list = [custom_filter]
        elif isinstance(custom_filter, list):
            # When it's a list, all elements of the list should be OgcExpressions. Raise otherwise.
            if any([not isinstance(x, OgcExpression) for x in custom_filter]):
                raise Exception('All elements of the custom filter list should be valid OgcExpressions')
            else:
                filter_list = [x for x in custom_filter]
        else:
            if custom_filter:
                raise Exception('Custom filter should be (a list of) valid OgcExpression(s)')
            else:
                filter_list = []

        filter_list.append(PropertyIsEqualTo(propertyname='code', literal=station_code))

        if start_date:
            filter_list.append(PropertyIsGreaterThanOrEqualTo(propertyname='timestamp', literal=start_date))

        if end_date:
            filter_list.append(PropertyIsLessThan(propertyname='timestamp', literal=end_date))

        # Convert filter to xml
        if len(filter_list) > 1:
            filterxml = etree.tostring(And(filter_list).toXML()).decode("utf-8")
        else:
            filterxml = etree.tostring(filter_list[0].toXML()).decode("utf-8")
        # Only request data for certain parameters
        if isinstance(parameter_list, list):
            if 'timestamp' not in parameter_list:
                parameter_list.append('timestamp')

            parameter_string = ','.join(parameter_list)

        else:
            parameter_string = None

        # Do the actual WFS request
        response = self.wfs.getfeature(typename=self.data_layer, filter=filterxml, outputFormat='csv',
                                       propertyname=parameter_string)

        # Convert to a clean dataframe
        df = pd.read_csv(response)
        df.drop(columns=['FID', 'the_geom', 'code'], inplace=True)
        df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
        df.set_index('timestamp', inplace=True)
        df.sort_index(inplace=True)

        return df


class AWS(Synop):

    def __init__(self, freq='H'):

        self.wfs = WebFeatureService(url='https://opendata.meteo.be/service/aws/ows', version='1.1.0')
        # AWS has no layer to fetch the available stations. So we grab them from the synop layer
        self.station_wfs = WebFeatureService(url='https://opendata.meteo.be/service/synop/wfs', version='1.1.0')
        self.stations = None
        if freq == 'H':
            self.data_layer = 'aws:aws_1hour'
        elif freq == 'D':
            self.data_layer = 'aws:aws_1day'
        elif freq == '10T':
            self.data_layer = 'aws:aws_10min'
        else:
            raise Exception('Freq string should be any of H (hourly), D (daily) or 10T (10 minute)')

    def get_stations(self):
        """
        Get the list of stations that are publicly available for requesting
        :return: pandas dataframe with the list of all stations
        """

        super().get_stations()
        # Only the data for station 'Zeebrugge' and 'Humain' are publicly available.
        # self.stations = self.stations[self.stations['name'].isin(['ZEEBRUGGE', 'HUMAIN'])]
        # Only the data from 2017-11-18 are publicly available.
        # self.stations['date_begin'] = '2017-11-18T00:00:00'

        return self.stations
