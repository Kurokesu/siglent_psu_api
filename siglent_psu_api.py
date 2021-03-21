__author__ = "Saulius Lukse"
__copyright__ = "Copyright 2015-2018, www.kurokesu.com"
__version__ = "0.1"
__license__ = "GNU GPLv3"

import socket
import sys
import time
from enum import Enum


class MODE(Enum):
    CV  = 1
    CC  = 2

class TRACK(Enum):
    INDEPENDENT  = 0
    SERIAL = 1
    PARALLEL = 2

class STATE(Enum):
    OFF = 0
    ON = 1

class CHANNEL(Enum):
    CH1 = 1
    CH2 = 2
    CH3 = 3

class PARAMETER(Enum):
    CURRENT = 1
    VOLTAGE = 2
    POWER = 3

class SIGLENT_PSU():

    def __init__(self, ip, port=5025):
        self.ip = ip
        self.port = port
        self._sleep = 1
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(1)
        self.s.connect((self.ip , self.port))

    def identify(self):
        self.s.sendall(b'*IDN?')
        #self.s.sendall(b'\n')
        reply = self.s.recv(4096).decode('utf-8').strip()
        reply = reply.split(",")
        reply_d = {}
        if len(reply) == 5:
            reply_d["manufacturer"] = reply[0]
            reply_d["model"] = reply[1]
            reply_d["sn"] = reply[2]
            reply_d["firmware_ver"] = reply[3]
            reply_d["hadrware_ver"] = reply[4]
            return reply_d
        return None

    def measure(self, ch, parameter):
        cmd = "MEASURE:" + parameter.name + "? " + ch.name
        cmd_b = cmd.encode("utf-8")
        self.s.sendall(cmd_b)
        #self.s.sendall(b'\n')
        time.sleep(self._sleep)
        reply = self.s.recv(4096).decode('utf-8').strip()
        reply = float(reply)
        return reply
   
    def set(self, ch, parameter, value):
        if parameter == PARAMETER.POWER:
            raise ValueError("Can't set POWER. Only VOLTAGE and CURRENT are supported.")

        if ch == CHANNEL.CH3:
            raise ValueError("Can't set output for CH3. Use mechanical selector on the instrument.")            

        cmd = ch.name + ":" + parameter.name + " " + str(value)
        cmd_b = cmd.encode("utf-8")
        self.s.sendall(cmd_b)
        #self.s.sendall(b'\n')
        time.sleep(self._sleep)

    def output(self, ch, status):
        cmd = "OUTPUT " + ch.name + "," + status.name
        cmd_b = cmd.encode("utf-8")
        self.s.sendall(cmd_b)
        #self.s.sendall(b'\n')
        time.sleep(self._sleep)

    def track(self, tr):
        cmd = "OUTPUT:TRACK " +  str(tr.value)
        cmd_b = cmd.encode("utf-8")
        self.s.sendall(cmd_b)
        #self.s.sendall(b'\n')
        time.sleep(self._sleep)

    def system(self):
        cmd = "SYSTem:STATus?"
        cmd_b = cmd.encode("utf-8")
        self.s.sendall(cmd_b)
        #self.s.sendall(b'\n')
        time.sleep(self._sleep)
        reply = self.s.recv(4096).decode('utf-8').strip()
        reply = int(reply, 16)

        response = {}
        if reply & 0x01:
            response["ch1_mode"] = MODE.CV
        else:
            response["ch1_mode"] = MODE.CC
        
        if reply & 0x02:
            response["ch2_mode"] = MODE.CV
        else:
            response["ch2_mode"] = MODE.CC

        m0 = reply & 0x04
        m1 = reply & 0x08

        if m0 and m1:
            response["mode"] = TRACK.SERIAL
        
        if m0 and not m1:
            response["mode"] = TRACK.INDEPENDENT

        if not m0 and m1:
            response["mode"] = TRACK.PARALLEL

        if reply & 0x10:
            response["ch1"] = STATE.ON
        else:
            response["ch1"] = STATE.OFF

        if reply & 0x20:
            response["ch2"] = STATE.ON
        else:
            response["ch2"] = STATE.OFF

        return response
