__author__ = "Saulius Lukse"
__copyright__ = "Copyright 2015-2018, www.kurokesu.com"
__version__ = "0.1"
__license__ = "GNU GPLv3"

import siglent_psu_api as siglent

s = siglent.SIGLENT_PSU("192.168.0.22")

# read instrument identification string
i = s.identify()
print(i)

# read instrument status
sys = s.system()
print(sys)


# Set output mode
#s.track(siglent.TRACK.INDEPENDENT)

# switch on CH1
s.output(siglent.CHANNEL.CH1, siglent.STATE.ON)

# set CH1 voltage to 2V
s.set(siglent.CHANNEL.CH1, siglent.PARAMETER.VOLTAGE, 2.0)

# read voltage
r = s.measure(ch = siglent.CHANNEL.CH1, parameter = siglent.PARAMETER.VOLTAGE)
print(r)
