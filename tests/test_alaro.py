from src.openkmi.grid_data import Alaro
from unittest import TestCase
import owslib


class TestAlaro(TestCase):

    def setUp(self):
        self.kmi = Alaro()

    def test_init(self):

        self.assertEqual(type(self.kmi.wms), owslib.map.wms130.WebMapService_1_3_0)

    def test_get_layers(self):

        self.assertEqual(len(self.kmi.get_parameters()), 35)

    def test_get_layer_abstract(self):

        self.assertEqual(self.kmi.get_parameter_info('2_m_temperature'), '2_m_temperature_height_above_ground')

    def test_get_layer_bbox(self):

        self.assertEqual(self.kmi.get_bbox('2_m_temperature'),
                         (-0.141525570620698, 47.37931567972357, 9.248525690604847, 53.640688592737376, 'CRS:84'))

    def test_get_data(self):

        tmp = self.kmi.get_data('2m_Relative_humidity', 4.6824, 52.3617)

        self.assertEqual(tmp.shape[0], 61)

    def test_projections(self):

        data_wgs = self.kmi.get_data('2m_Relative_humidity', 4.6824, 52.3617)
        data_lamb = self.kmi.get_data('2m_Relative_humidity', 169955, 338336, epsg='31370')
        data_3857 = self.kmi.get_data('2m_Relative_humidity', 519037, 6862188, epsg='3857')

        self.assertEqual(data_wgs.iloc[0, 0], data_lamb.iloc[0, 0])
        self.assertEqual(data_3857.iloc[0, 0], data_lamb.iloc[0, 0])
