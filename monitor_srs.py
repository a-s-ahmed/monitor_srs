import serial
import time
from prometheus_client import start_http_server, Summary, Gauge
import pandas as pd
import os
import numpy as np

"""
This program repeatedly queries the IGC 100 controller for IG1 and PG1 values and exposes it via prometheus to Grafana which we then setup to monitor
and alert us depending on the pressure leaving a certain value 

Version 1.0 - Ahmed Ahmed (asahmed2@ualberta.ca). Feel free to email me for help adapting this or expanding it to deal with multiple controllers.
"""

#Initialize serial comm
port_name = input("/dev/ttyUSB0")    
ser = serial.Serial(
      port = port_name,
      baudrate = 115200,
      parity = serial.PARITY_NONE,
      bytesize = serial.EIGHTBITS,
      stopbits = serial.STOPBITS_ONE,
      xonxoff = 0,
      rtscts = 0,
      timeout = 1
)
ser.close()
ser.open()


#Initialize Prometheus Gauges
pg_gauge = Gauge('Test_PG',unit='Torr',documentation="Readings from PG 1")
ig_gauge = Gauge('Test_IG',unit='Torr',documentation="Readings from IG 1")


#Every 10 seconds query IG or PG depending on value of bool ig. sleep for 1 second before getting response just incase.
ig = True

if __name__ == '__main__':
    # Start up the server to expose the metrics on port 8000.
    start_http_server(8000)

    while True:
        time.sleep(10)
        if(ig==True){
            # We query and expose IG 
            ser.write( str.encode('GDAT? 1\r\n'))
            #ig = False
        }
        else{
            # We query and expose PG and set ig to true for next time
            ser.write( str.encode('GDAT? 3\r\n'))
            #ig = True
        }

        time.sleep(1)
        out = ''
        while ser.inWaiting() > 0:
                while True:
                    # Check if trash is being received from the RS-232 such as %$///#@@ or Chinese characters
                    try:
                        # Append all of the received bytes into a single string
                        out += ser.read().decode('ascii') #python > 2.7
                        #out += ser.read()                 #python <= 2.7
                        break
                    except ValueError:
                        out = ''
            
        if out != '':
            #Expose readings.
            try:
               # print(str(out))
                if(ig == True){
                    #our out is IG, so expose it as such, else expose as PG. Regardless, we switch IG's value.
                    print("IG")
                    print(float(out)
                    ig_gauge.set(float(out))
                    ig = False
                }else{
                    print("PG")
                    print(float(out)
                    pg_gauge.set(float(out))
                    ig = True
                }
               
                
            except:
                print("Keyboard Interrupt")
                break
            