from src.pykmi.synoptic import Synop
from unittest import TestCase
import owslib


class TestpyKMI(TestCase):

    def setUp(self):
        self.kmi = Synop()

    def test_init(self):

        self.assertEqual(type(self.kmi.wfs), owslib.feature.wfs110.WebFeatureService_1_1_0)

    def test_get_stations(self):

        self.assertEqual(self.kmi.get_stations().shape[0], 22)

    def test_get_params(self):

        self.assertEqual(len(self.kmi.get_parameters()), 19)

    def test_get_data(self):

        df_r = self.kmi.get_data('6438', start_date='2015-01-01T00:00:00', end_date='2015-01-02T00:00:00',
                                 parameter_list=['wind_speed'])

        self.assertAlmostEqual(df_r.sum()['wind_speed'], 156.872, places=3)
        self.assertEqual(df_r.shape[0], 24)

    def test_wrong_station(self):

        with self.assertRaises(Exception) as context:
            self.kmi.get_data('notavalidstation', start_date='2015-01-01T00:00:00',
                              end_date='2015-01-02T00:00:00', parameter_list=['wind_speed'])

        self.assertTrue('station code not valid' in str(context.exception))

