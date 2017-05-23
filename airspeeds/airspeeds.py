"""
GUI that shows conversion from IAS to EAS and TAS with altitude
"""
import math
import numpy as np
from appJar import gui


def ias_to_tas(speed, altitude):
    """
    Converts Indicated Airspeed (IAS) to True Airspeed (TAS)
    :param speed: speed: Int/Float of an indicated airspeed
    :param altitude: Altitude as an int in feet (ex, 35,000 ft is 35000)
    :return: Float of the equivalent airspeed, float of the true airspeed
    TAS = IAS x sqrt(rho_0/rho)
    """
    if altitude > 70000 or altitude < 0:
        app.errorBox("Altitude out of bounds!",
                     "This app only functions when the altitude is between 0 and 70,000 feet.")
    else:
        rho_0 = 23.77E-04  # slug/ft^3
        alt_to_density = {          # Feet :  slug/ft^3
            0: 23.77E-4,    # data from: http://www.engineeringtoolbox.com/standard-atmosphere-d_604.html
            5000: 20.48E-4,
            10000: 17.56E-4,
            15000: 14.96E-4,
            20000: 12.67E-4,
            25000: 10.66E-4,
            30000: 8.91E-4,
            35000: 7.38E-4,
            40000: 5.87E-4,
            45000: 4.62E-4,
            50000: 3.64E-4,
            55000: 2.95E-4,
            60000: 2.26E-4,
            65000: 1.825E-4,
            70000: 1.39E-4,
        }

        if altitude in list(alt_to_density.keys()):
            rho = alt_to_density[altitude]
            true_airspeed = round(speed * math.sqrt(rho_0 / rho))
        else:
            altitude_sensitivity = 5000.0
            upper_limit = math.ceil(altitude / altitude_sensitivity) * altitude_sensitivity
            lower_limit = upper_limit - altitude_sensitivity
            rho = np.interp(altitude, [lower_limit, upper_limit],
                            [alt_to_density[lower_limit], alt_to_density[upper_limit]])
            true_airspeed = round(speed * math.sqrt(rho_0 / rho))

        return true_airspeed


def press(btn):
    if btn == "Cancel":
        app.stop()
    else:
        knots_to_mph = 1.15078
        ias = float(app.getEntry("indicated"))
        altitude = float(app.getEntry("altitude"))
        tas = ias_to_tas(ias, altitude)
        app.setLabel("true2", tas)
        app.setLabelRelief("true2", "raised")
        app.setLabelAlign("true2", "left")
        try:
            filler = round(tas * knots_to_mph)
        except TypeError:
            filler = 0
        app.setLabel("mph2", filler)
        app.setLabelRelief("mph2", "raised")
        app.setLabelAlign("mph2", "left")

#     Main startup
app = gui("Airspeed Calculator", "500x300")
app.setFont(20)

app.addLabel("title", "Airspeed Calculator", 0, 0, 2)       # Row 0,Column 0,Span 2
app.setFont(14)
app.addLabel("indicated", "Indicated Airspeed (Knots): ", 1, 0)     # Row 1, Column 0
app.setLabelAlign("indicated", "left")
app.addNumericEntry("indicated", 1, 1)                             # Row 1,Column 1
app.addLabel("altitude", "Altitude (feet):", 2, 0)                 # Row 2,Column 0
app.setLabelAlign("altitude", "left")
app.addNumericEntry("altitude", 2, 1)                            # Row 2,Column 1
app.addLabel("true", "True airspeed (Knots):", 3, 0)
app.addLabel("true2", "", 3, 1)
app.setLabelAlign("true", "left")
app.addLabel("mph", "True airspeed (MPH):", 4, 0)
app.addLabel("mph2", "", 4, 1)
app.setLabelAlign("mph", "left")


app.addButtons(["Submit", "Cancel"], press, 6, 0, 2)        # Row 3,Column 0,Span 2


app.setEntryFocus("indicated")
app.go()
