from owslib.fes import PropertyIsEqualTo, PropertyIsGreaterThanOrEqualTo, PropertyIsLessThan, And
from owslib.wfs import WebFeatureService
from owslib.etree import etree
import pandas as pd


WFS_ENDPOINT = 'https://opendata.meteo.be/service/synop/wfs'


class Synop:

    def __init__(self):

        self.wfs = WebFeatureService(url=WFS_ENDPOINT, version='1.1.0')
        self.stations = None

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
        response = self.wfs.getfeature(typename='synop:synop_station', outputFormat='csv')
        df_stations = pd.read_csv(response)
        df_stations.drop(columns=['FID'], inplace=True)
        df_stations['code'] = df_stations['code'].astype('str')
        self.stations = df_stations

        return df_stations

    def get_parameters(self):
        """
        Get parameters that we can request for the stations
        :return: dictionary with the parameters
        """
        return self.wfs.get_schema('synop:synop_data')['properties']

    def get_data(self, station_code, start_date=None, end_date=None, parameter_list=None):
        """
        Return the data for a station
        :param station_code: station code
        :param start_date: start date for which to request the data (string, format: '2021-01-01T00:00:00')
        :param end_date: end date for which to request the data (string, format: '2021-01-01T00:00:00')
        :param parameter_list: List of parameters
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
        filter_list = [PropertyIsEqualTo(propertyname='code', literal=station_code)]

        if start_date:
            filter_list.append(PropertyIsGreaterThanOrEqualTo(propertyname='timestamp', literal=start_date))

        if end_date:
            filter_list.append(PropertyIsLessThan(propertyname='timestamp', literal=end_date))

        # Convert filter to xml
        filterxml = etree.tostring(And(filter_list).toXML()).decode("utf-8")

        # Only request data for certain parameters
        if isinstance(parameter_list, list):
            if 'timestamp' not in parameter_list:
                parameter_list.append('timestamp')

            parameter_string = ','.join(parameter_list)

        else:
            parameter_string = None

        # Do the actual WFS request
        response = self.wfs.getfeature(typename='synop:synop_data', filter=filterxml, outputFormat='csv',
                                       propertyname=parameter_string)

        # Convert to a clean dataframe
        df = pd.read_csv(response)
        df.drop(columns=['FID', 'the_geom', 'code'], inplace=True)
        df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
        df.set_index('timestamp', inplace=True)
        df.sort_index(inplace=True)

        return df