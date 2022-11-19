# Importing Required modules 
import time  
import sys 
import  wiotp.sdk.device# IBM IoT Watson Platform Module
import ibmiotf.device
import tkinter as tk # Python GUI Package  
from tkinter import ttk # Python GUI 
import time 
from threading import Thread 
 
 
organization = "0tus0f" # Organization ID 
deviceType = "ESP32"   # Device type 
deviceId = "01"    # Device ID 
authMethod = "token"    # Authentication Method 
authToken = "Gowth@m@nk18" #Replace the authtoken 
 
 
# Tkinter root window 
root = tk.Tk() 
root.geometry('350x300')  # Set size of root window 
root.resizable(False, False) # root window non-resizable 
root.title('Gas Leakage Monitoring And Alerting System for Industries (PNT2022TMID42277)') 
 
 
# Layout Configurations 
root.columnconfigure(0, weight=1) 
root.columnconfigure(1, weight=3) 
 
 
current_gas = tk.DoubleVar() 

def get_current_gas(): # function returns current gas level value 
    return '{: .2f}'.format(current_gas.get()) 
     
def slider_changed(event): # Event Handler for changes in sliders 
    print('--------') 
    print('Gas Level: {: .2f}'.format(current_gas.get())) 
    print('--------') 
    gas_label.configure(text=str(get_current_gas()) +" ppm")  # Displays current gas level as label content 

 
# Tkinter Labels 
 
# label for the gas level slider 
slider_gas_label = ttk.Label(root,text='Set Gas Level:') 
slider_gas_label.grid(column=0,row=0,sticky='w') 
 
 
#  Gas Level slider 
slider_gas = ttk.Scale(root,from_=0,to=3000,orient='horizontal',  command=slider_changed,variable=current_gas) 
slider_gas.grid(column=1,row=0,sticky='we') 
 
 
# current gas level label 
current_gas_label = ttk.Label(root,text='Current Gas Level:') 
current_gas_label.grid(row=1,columnspan=2,sticky='n',ipadx=10,ipady=10) 
 
 
# Gas level label (value gets displayed here) 
gas_label = ttk.Label(root,text=str(get_current_gas()) +" ppm") 
gas_label.grid(row=2,columnspan=2,sticky='n')
 
 
def publisher_thread(): 
    thread = Thread(target=publish_data) 
    thread.start() 
 
def publish_data():
    # Exception Handling 
    try: 
        deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, 
                         "auth-token": authToken} 
        deviceCli = ibmiotf.device.Client(deviceOptions) 
    # .............................................. 
 
    except Exception as e: 
        print("Caught exception connecting device: %s" % str(e)) 
        sys.exit() 
 
    deviceCli.connect()  # Connect to IBM Watson IoT Platform 
 
    while True: 
        gas_level = int(current_gas.get()) 
 
        data = {'gas_level' : gas_level} 
 
        def myOnPublishCallback(): 
            print("Published Gas Level = %s ppm" % gas_level, "to IBM Watson") 
 
        success = deviceCli.publishEvent("event", "json", data, qos=0, on_publish=myOnPublishCallback) 
        if not success: 
            print("Not connected to IoTF") 
        time.sleep(1) 
 
publisher_thread() 
 
root.mainloop() # startup Tkinter GUI 
 
# Disconnect the device and application from the cloud 
deviceCli.disconnect()
