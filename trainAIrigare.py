#!/usr/bin/env python

import pexpect, sys, json, select, MySQLdb
from time import time
#from sensor_calcs import *
# LoPoSwitch

# function to transform hex string like "0a cd" into signed integer
def hexStrToInt(hexstr):
    val = int(hexstr[0:2],16) + (int(hexstr[3:5],16)<<8)
    if ((val&0x8000)==0x8000): # treat signed 16bits
        val = -((val^0xffff)+1)
    return val


def floatfromhex(h):
    t = float.fromhex(h)
    if t > float.fromhex('7FFF'):
        t = -(float.fromhex('FFFF') - t)
        pass
    return t

class LoPoSwitch:
	file = "/tmp/LoPoSwitch.log"

	def __init__( self, bluetooth_adr ):
		self.con = pexpect.spawn('gatttool -b ' + bluetooth_adr + ' --interactive -t random --listen')
		self.con.logfile = open(self.file, "a")
		self.con.expect('\[LE\]>', timeout=100)
		print "Preparing to connect."
		self.con.sendline('connect')
		# test for success of connect
		self.con.expect('Connection successful.*\[LE\]>')
		# Earlier versions of gatttool returned a different message.  Use this pattern -
		#self.con.expect('\[CON\].*>')
		self.cb = {}
		self.con.sendline('char-write-req 0x000e 0100')
		self.con.expect('Characteristic value was written successfully')
		self.cb = {}
		return

	def turnOn(self):
		self.con.sendline('connect') # Reconnect if not connected
		self.cb = {}
                self.con.sendline('char-write-req 0x000e 0100')
		self.con.expect('Characteristic value was written successfully')

		cmd = 'char-write-cmd 0x000b 5231' #Write 'R1' to second attribute
		#print cmd
		self.con.sendline( cmd )
		self.con.expect("\[LE\].*>")
		self.cb = {}
		return

	def turnOff(self):
		self.con.sendline('connect') # Reconnect if not connected
                self.cb = {}
                self.con.sendline('char-write-req 0x000e 0100')
                self.con.expect('Characteristic value was written successfully')
		
		cmd = 'char-write-cmd 0x000b 5230' #Write 'R0' to second attribute
		#print cmd
		self.con.sendline( cmd )
		self.con.expect("\[LE\].*>")
		self.cb = {}
		return

	def writeLog():
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
    #Pump.writeLog(wT)

#if __name__ == "__main__":
#    main()

