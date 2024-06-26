#!/usr/bin/env python
#-----------------------------------------------------------------------------
# A simple test to speed up and slow down 1 motor.
#------------------------------------------------------------------------
#
# Written by Mark Lindemer
# SparkFun Electronics, April 2020
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#==================================================================================
# Example 1
#

from __future__ import print_function
import time
import sys
import math
import qwiic_scmd

#jwc add encoder
import qwiic_dual_encoder_reader


myMotor = qwiic_scmd.QwiicScmd()

def runExample():

    # Motor Setup
    #
    ###jwc o print("Motor Test.")
    R_MTR = 0
    L_MTR = 1
    FWD = 0
    BWD = 1
    
    if myMotor.connected == False:
        print("Motor Driver not connected. Check connections.", \
            file=sys.stderr)
        return
    print("Motors Setup 1of3: Connected.")
    
    myMotor.begin()
    time.sleep(.250)
    print("Motors Setup 2of3: Initialized.")
    
    # Zero Motor Speeds
    myMotor.set_drive(0,0,0)
    myMotor.set_drive(1,0,0)
    myMotor.enable()
    time.sleep(.250)
    print("Motors Setup 3of3: Enabled H-Bridge Circuit")

    # Encoder Setup
    #
    ###jwc o print("\nSparkFun Qwiic Dual Encoder Reader   Example 1\n")
    myEncoders = qwiic_dual_encoder_reader.QwiicDualEncoderReader()
    if myEncoders.connected == False:
        print("The Qwiic Dual Encoder Reader device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    print("Encoders Setup 1of3: Connected.")
    
    myEncoders.begin()
    print("Enocders Setup 2of3: Initialized.")
    
    #jwc Print 'Limit/Max'.  
    if myEncoders.limit == 0:
        print("*** Limit:32767 ticks (Default)")
    else:
        print("*** Limit: %d ticks" % (myEncoders.limit))
    #jwc Clear Counters of any residue values: Important since Counters seem to have persistent memory of last program ran
    #
    myEncoders.set_count1(0)
    myEncoders.set_count2(0)
    print("Enocders Setup 3of3: Show Encoder Limit -&- Clear Encoder Values.")


    while True:
        speed = 20

        for speed in range(20,255):
            ###jwc o print(speed)
            myMotor.set_drive(R_MTR,FWD,speed)
            
            ###jwc add:
            myMotor.set_drive(L_MTR,FWD,speed)

            print("Speed: %d || Count1: %d | Count2: %d" % (speed, myEncoders.count1, myEncoders.count2))
            ###jwc withhold from encoder example: # Delay in Seconds: 0.3sec = 300msec
            ###jwc withhold from encoder example: time.sleep(.3)
            
            # Delay in Seconds: 0.05sec = 50msec 
            time.sleep(.05)

        for speed in range(254,20, -1):
            ###jwc o print(speed)
            myMotor.set_drive(R_MTR,FWD,speed)
            
            ###jwc add:
            myMotor.set_drive(L_MTR,FWD,speed)

            print("Speed: %d || Count1: %d | Count2: %d" % (speed, myEncoders.count1, myEncoders.count2))
            ###jwc withhold from encoder example: # Delay in Seconds: 0.3sec = 300msec
            ###jwc withhold from encoder example: time.sleep(.3)

            # Delay in Seconds: 0.05sec = 50msec
            time.sleep(.05)

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("Ending example.")
        myMotor.disable()
        sys.exit(0)
