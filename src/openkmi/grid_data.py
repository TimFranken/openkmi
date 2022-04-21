from owslib.fes import PropertyIsEqualTo, PropertyIsGreaterThanOrEqualTo, PropertyIsLessThan, And, OgcExpression
from owslib.wms import WebMapService
from owslib.etree import etree
import pandas as pd
import json
from pyproj import Proj, transform
from pyproj import Transformer
import matplotlib.pyplot as plt


class Alaro:

    def __init__(self):

        self.wms = WebMapService(url='https://opendata.meteo.be/service/alaro/ows', version='1.3.0')

    def get_layers(self):
        """
        Get the layers we can use in the WMS
        :return: list of layers
        """
        return list(self.wms.contents.keys())

    def get_layer_times(self, layer_name):
        """
        Get a pandas date index with all the available dates we can request
        :return: pandas date index with all available dates
        """
        layer = self.wms.contents[layer_name]
        tp = layer.timepositions[0].split('/')
        date_index = pd.date_range(start=tp[0], end=tp[1], freq=tp[-1][-2:])

        return date_index

    def get_layer_crs(self, layer_name):
        """
        Get an overview of all the crs options available
        :return: list of layers
        """
        layer = self.wms.contents[layer_name]

        return layer.crsOptions

    def get_layer_abstract(self, layer_name):
        """
        Get the layer abstract
        :return: list of layers
        """
        layer = self.wms.contents[layer_name]

        return layer.abstract

    def get_layer_bbox(self, layer_name):
        """
        Get the bounding box
        :return: list of layers
        """
        layer = self.wms.contents[layer_name]

        return layer.boundingBox

    def get_data(self, layer_name, x, y, epsg='4326'):
        """
        Get all the data for a particular timeframe
        :return: list of layers
        """

        tts = self.get_layer_times(layer_name)

        df = pd.DataFrame(index=tts, columns=[layer_name])

        region_size = (4000, 4000)

        if epsg == '3857':
            x_t, y_t = x, y
        else:
            transformer = Transformer.from_crs(f"epsg:{epsg}", "epsg:3857", always_xy=True)
            x_t, y_t = transformer.transform(x, y)

        xupper = int(round(x_t - region_size[0] / 2))
        xlower = int(round(x_t + region_size[0] / 2))
        yupper = int(round(y_t - region_size[1] / 2))
        ylower = int(round(y_t + region_size[1] / 2))

        bbox = (xupper, yupper, xlower, ylower)

        for i in df.index:
            info = self.wms.getfeatureinfo(
                layers=[layer_name],
                query_layers=[layer_name],
                srs='EPSG:3857',
                bbox=bbox,
                size=region_size,
                info_format='application/json',
                time=i.strftime('%Y-%m-%dT%H:%M:%SZ'),
                xy=(0, 0)
            )

            tmp = json.loads(info.read())

            df.loc[i, layer_name] = list(tmp['features'][0]['properties'].values())[0]

        return df

aa = Alaro()
print(aa.get_layers())
tmp = aa.get_data('2_m_temperature', 4.62, 50.72)
tmp.plot()
plt.show()
