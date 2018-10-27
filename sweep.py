__author__ = "Saulius Lukse"
__copyright__ = "Copyright 2015-2018, www.kurokesu.com"
__version__ = "0.1"
__license__ = "GNU GPLv3"

import siglent_psu_api as siglent
import numpy as np

s = siglent.SIGLENT_PSU("192.168.0.22")

# read instrument identification string
i = s.identify()
print(i)

# read instrument status
sys = s.system()
print(sys)

# switch on CH1
s.output(siglent.CHANNEL.CH1, siglent.STATE.ON)

# sweep specified range
range_min = 1
range_max = 5
range_step = 0.1
ra = np.arange(range_min, range_max, range_step)
for i in ra:
    s.set(siglent.CHANNEL.CH1, siglent.PARAMETER.VOLTAGE, i)
    r = s.measure(ch = siglent.CHANNEL.CH1, parameter = siglent.PARAMETER.POWER)
    print(r)
