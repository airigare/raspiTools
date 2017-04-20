#!/usr/bin/env python

import pexpect, sys, json, select, MySQLdb
from time import time
#from sensor_calcs import *
# LoPoSwitch
def floatfromhex(h):
    t = float.fromhex(h)
    if t > float.fromhex('7FFF'):
        t = -(float.fromhex('FFFF') - t)
        pass
    return t

class LoPoSwitch:
	def __init__( self, bluetooth_adr ):
		self.con = pexpect.spawn('gatttool -b ' + bluetooth_adr + ' --interactive -t random --listen')
		self.con.expect('\[LE\]>', timeout=100)
		print "Preparing to connect."
		self.con.sendline('connect')
		# test for success of connect
		self.con.expect('Connection successful.*\[LE\]>')
		# Earlier versions of gatttool returned a different message.  Use this pattern -
		#self.con.expect('\[CON\].*>')
		self.cb = {}
		self.con.sendline('char-write-req 0x000e 0100')
		self.cb = {}
		return

	def turnOn(self):
		self.con.sendline('connect') # Reconnect if not connected
		cmd = 'char-write-cmd 0x000b 5231' #Write 'R1' to second attribute
		print cmd
		self.con.sendline( cmd )
		print(child.before)
		self.cb = {}
		return

	def turnOff(self):
		self.con.sendline('connect') # Reconnect if not connected

		cmd = 'char-write-cmd 0x000b 5230' #Write 'R0' to second attribute
		print cmd
		self.con.sendline( cmd )
		print(child.before)
		return

	def writeLog(t):
		print("Data logged successefully")
		return -1




bluetooth_adr = "CB:FE:19:98:A0:EF"
Pump = LoPoSwitch(bluetooth_adr)
while True:
    var = input("Start Watering? \nType <<1>> to start or <<10>> to exit: ")

    if var == 10:
        sys.exit()

    if var != 1 :
        continue

    Pump.turnOn()
    sT = time()

    while var == 1:
        var = input("Stop Watering? \n Type <<0>> to stop: ")

    Pump.turnOff()
    wT = time() - sT
    print("I was watering " + str(round(wT,0)) + " seconds")
    writeLog(wT)

#if __name__ == "__main__":
#    main()

