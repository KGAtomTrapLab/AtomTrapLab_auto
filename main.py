from matplotlib import pyplot as plt
import peak_detection
import heatmaps_function
import numpy as np
'''
Import functions from peak_detection.py and heatmaps_function.py
INPUT:
    CSV Text file of data (columns must correspond)
        --> Must include(IN ORDER):
            "Saturated Absorption", "NA", "Error", "NaN", "Voltage"
            (1) Saturated Absorption
            (2) Fabry Perot
            (3) Error
            (4) NaN (Fabry Perot?)
            (5) Voltage
            Note-- Fabry Perot is input in the line:
                conv, q = heatmaps_function.fabry_perot_conversions(df["Fabry Perot"],df)
            
'''
