from owslib.wms import WebMapService
import pandas as pd
import json
from pyproj import Transformer


class Alaro:

    def __init__(self):

        self.wms = WebMapService(url='https://opendata.meteo.be/service/alaro/ows', version='1.3.0')

    def get_parameters(self):
        """
        Get the parameters we can use in the WMS
        :return: list of parameters
        """
        return list(self.wms.contents.keys())

    def get_times(self, parameter_name):
        """
        Get a pandas date index with all the available dates we can request
        :param parameter_name: parameter to query
        :return: pandas date index with all available dates
        """
        layer = self.wms.contents[parameter_name]
        tp = layer.timepositions[0].split('/')
        date_index = pd.date_range(start=tp[0], end=tp[1], freq=tp[-1][-2:])

        return date_index

    def get_parameter_info(self, parameter_name):
        """
        Get the parameter abstract
        :param parameter_name: parameter to query
        :return: abstract from the corresponding layer
        """
        layer = self.wms.contents[parameter_name]

        return layer.abstract

    def get_bbox(self, parameter_name):
        """
        Get the bounding box of the parameter
        :param parameter_name: parameter to query
        :return: tuple with bounding box
        """
        layer = self.wms.contents[parameter_name]

        return layer.boundingBox

    def get_data(self, parameter_name, x, y, epsg='4326'):
        """
        Retrieve all the forecasts for a certain parameter and location
        :param parameter_name: layer to query
        :param x: x-coordinate for which to retrieve data
        :param y: y-coordinate for which to retrieve data
        :param epsg: EPSG-code of the X-Y coordinates that are given. Default is WGS84
        :return: pandas dataframe with value of the layer for all available forecasting times
        """

        # Create empty dataframe with available times
        df = pd.DataFrame(index=self.get_times(parameter_name), columns=[parameter_name])

        # Transform coordinates to EPSG:3857 that is used in the request
        if epsg == '3857':
            x_t, y_t = x, y
        else:
            transformer = Transformer.from_crs(f"epsg:{epsg}", "epsg:3857", always_xy=True)
            x_t, y_t = transformer.transform(x, y)

        # Fetch the data
        region_size = (2, 2)
        xupper = int(round(x_t - region_size[0] / 2))
        xlower = int(round(x_t + region_size[0] / 2))
        yupper = int(round(y_t - region_size[1] / 2))
        ylower = int(round(y_t + region_size[1] / 2))

        bbox = (xupper, yupper, xlower, ylower)

        for i in df.index:
            info = self.wms.getfeatureinfo(
                layers=[parameter_name],
                query_layers=[parameter_name],
                srs='EPSG:3857',
                bbox=bbox,
                size=region_size,
                info_format='application/json',
                time=i.strftime('%Y-%m-%dT%H:%M:%SZ'),
                xy=(0, 0)
            )

            data_value = json.loads(info.read())

            df.loc[i, parameter_name] = list(data_value['features'][0]['properties'].values())[0]

        return df
