from src.openkmi.synoptic import Synop
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

    def test_custom_filter(self):

        from owslib.fes import PropertyIsEqualTo

        custom_filt = PropertyIsEqualTo(propertyname='precip_range', literal='2')
        df_r = self.kmi.get_data('6447', start_date='2020-01-01T00:00:00', end_date='2021-01-01T00:00:00',
                                 parameter_list=['precip_quantity', 'precip_range'], custom_filter=custom_filt)

        self.assertEqual(df_r.shape[0], 366*2)

    def test_wrong_station(self):

        with self.assertRaises(Exception) as context:
            self.kmi.get_data('notavalidstation', start_date='2015-01-01T00:00:00',
                              end_date='2015-01-02T00:00:00', parameter_list=['wind_speed'])

        self.assertTrue('station code not valid' in str(context.exception))

    def test_wrong_custom_filter(self):

        with self.assertRaises(Exception) as context:
            self.kmi.get_data('6447', start_date='2015-01-01T00:00:00',
                              end_date='2015-01-02T00:00:00', parameter_list=['wind_speed'],
                              custom_filter='thisisnotafilter')

        self.assertTrue('OgcExpression' in str(context.exception))

    def test_wrong_custom_filter_list(self):

        from owslib.fes import PropertyIsEqualTo

        custom_filt = PropertyIsEqualTo(propertyname='precip_range', literal='2')

        with self.assertRaises(Exception) as context:
            self.kmi.get_data('6447', start_date='2015-01-01T00:00:00',
                              end_date='2015-01-02T00:00:00', parameter_list=['wind_speed'],
                              custom_filter=[custom_filt, 'thisisnotafilter'])

        self.assertTrue('OgcExpression' in str(context.exception))

    def test_no_options(self):

        df_r = self.kmi.get_data('6438')

        self.assertEqual(df_r.first_valid_index().year, 2012)
        self.assertEqual(df_r.shape[1], 17)
