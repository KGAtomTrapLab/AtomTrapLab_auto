import unittest
import heatmaps_function

class TestHeatmaps_function(unittest.TestCase):

	def test_fabry_perot_conversion(self):
		self.assertEqual(heatmaps_function.fabry_perot_conversion(fsr), expected)

	def test_raw_to_frequency_coords(self):
		self.assertEqual(heatmaps_function.raw_to_frequency_coords(raw_coords,conv,df), peak_freq)

	def test_frequency_percent_difference(self):
		self.assertEqual(heatmaps_function.frequency_percent_difference(peak_freq)[Rb87t_perc,Rb87p_perc,Rb85t_perc,Rb85_perc])

	def test_frequency_intervals(self):
		self.assertEqual(heatmaps.function.frequency_intervals(peak_freq),interval)

	def test_interval_percent_difference(self):
		self.assertEqual(heatmaps.function.interval_percent_difference(interval),[Rb87t_pint,Rb87p_pint,Rb85t_pint,Rb85_pint])

	def test_error_val(self):
		self.assertEqual(heatmaps.function.error_val(raw_coords,df),error)

if __name__  == '__main__':
	unittest.main()