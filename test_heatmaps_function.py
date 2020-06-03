import unittest
import heatmaps_function
import pandas as pd
# Import Test Data
df = pd.read_csv("testScan.txt", header=None, sep='\t')
df.columns = ['Saturated Absorption','NA', 'Error', 'NaN', 'Voltage']
for i in range(3):
    df['Saturated Absorption'][i] = 0

# a = heatmaps_function.error_val(1,[(100,0.9),(200,0.9),(300,0.9),(400,0.9),(500,0.9),(600,0.9)],df,.02)
# print(a)

class TestHeatmaps_function(unittest.TestCase):

	# def test_fabry_perot_conversion(self):
	# 	self.assertEqual(heatmaps_function.fabry_perot_conversion(fsr), expected)

	# def test_raw_to_frequency_coords(self):
	# 	self.assertEqual(heatmaps_function.raw_to_frequency_coords(raw_coords,conv,df), peak_freq)

	def test_frequency_percent_difference(self):
		self.assertEqual(heatmaps_function.frequency_percent_difference([0,100,200,300,400,500]),([25.0936329588015, 5.660377358490567, 12.359550561797752, 15.77424023154848, 17.92452830188679], [27.388535031847134, 74.67248908296943, 91.0828025477707, 107.25388601036269, 118.3406113537118], [65.28925619834712, 117.3913043478261, 147.93388429752065, 162.29508196721312, 171.73913043478262], [217.46031746031744, 334.7826086956522, 376.1904761904762, 416.1290322580645, 443.47826086956525]))

	def test_frequency_intervals(self):
		self.assertEqual(heatmaps_function.frequency_intervals([0,110,200,310,400,510]),([110, 90, 110, 90, 110]))  #else case
		self.assertEqual(heatmaps_function.frequency_intervals([0,110,100,310,400,510]),([110]))  #case where list is not in increasing order.
		self.assertEqual(heatmaps_function.frequency_intervals([0,100,110,310,300,510]),([100,10,200]))  #case where list is not in increasing order.

	def test_interval_percent_difference(self):
		self.assertEqual(heatmaps_function.interval_percent_difference([0,110,200,310,400,510]),([100.0, 40.12738853503185, 263.6363636363636, 294.90445859872614, 409.5541401273885], [100.0, 205.55555555555554, 370.5882352941177, 761.1111111111111, 1011.1111111111111], [100.0, 249.20634920634922, 589.655172413793, 884.1269841269842, 1169.8412698412699], [100.0, 658.6206896551724, 1076.4705882352941, 2037.9310344827586, 2658.620689655172]))

	def test_lowest_perc_diff(self):
		self.assertEqual(heatmaps_function.lowest_perc_diff(10,20,30,40,10,20,30,40),1)
		self.assertEqual(heatmaps_function.lowest_perc_diff(20,10,30,40,20,10,30,40),2)

	def test_error_val(self):
		self.assertEqual(heatmaps_function.error_val(1,[(100,0.9),(200,0.9),(300,0.9),(400,0.9),(500,0.9),(600,0.9)],df,.02),-0.021)

if __name__  == '__main__':
	unittest.main()
