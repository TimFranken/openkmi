from src.openkmi.point_obs import AWS
from unittest import TestCase
import owslib


class TestAws(TestCase):

    def setUp(self):
        self.kmi = AWS()

    def test_init(self):

        self.assertEqual(type(self.kmi.wfs), owslib.feature.wfs110.WebFeatureService_1_1_0)

    def test_get_stations(self):

        self.assertEqual(self.kmi.get_stations().shape[0], 2)

    def test_get_params(self):

        self.assertEqual(len(self.kmi.get_parameters()), 8)

    def test_get_hourly_data(self):

        df_r = self.kmi.get_data('6472', start_date='2022-02-01T00:00:00', end_date='2022-02-05T00:00:00',
                                 parameter_list=['wind_speed'])

        self.assertAlmostEqual(df_r.mean()['wind_speed'], 5.073, places=3)
        self.assertEqual(df_r.shape[0], 24*4)

    def test_get_daily_data(self):

        kmi_d = AWS(freq='D')
        df_r = kmi_d.get_data('6472', start_date='2022-02-01T00:00:00', end_date='2022-02-05T00:00:00',
                                 parameter_list=['wind_speed'])

        self.assertAlmostEqual(df_r.mean()['wind_speed'], 5.0, places=3)
        self.assertEqual(df_r.shape[0], 4)

    def test_get_10T_data(self):

        kmi_10t = AWS(freq='10T')
        df_r = kmi_10t.get_data('6472', start_date='2022-02-01T00:00:00', end_date='2022-02-05T00:00:00',
                                 parameter_list=['wind_speed'])

        self.assertAlmostEqual(df_r.mean()['wind_speed'], 5.087, places=3)
        self.assertEqual(df_r.shape[0], 4*24*6)

    def test_wrong_freq(self):

        with self.assertRaises(Exception) as context:
            kmi_nofreq = AWS(freq='paktmaar10minuten')

        self.assertTrue('Freq string should be any' in str(context.exception))

