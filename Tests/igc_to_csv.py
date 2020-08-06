import serial
import time
import csv
import numpy as np
import os
#This file is meant to test automatic IGC100 querying by saving queries to a "test_data.csv" in this directory continuously until stopped

csv_path = os.path.dirname(os.path.abspath(__file__)) + "\\test_data.csv"

#Get COM port name and initialize serial comm
port_name = input("Enter a port name: ")    
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



#Every half a second query the IGC for a PG Mono Guage reading
while True:
    ser.write( str.encode('GDAT?4\r\n'))
    time.sleep(0.5)
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
        #Print values to our file until we interrupt
        try:
            print(str(out))
            with open(csv_path,"a", newline='') as f:
                writer = csv.writer(f,delimiter=",")
                writer.writerow([time.time(),out])
            
        except:
            print("Keyboard Interrupt")
            break