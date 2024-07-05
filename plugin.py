# Chirpstack 2 domoticz : a plugin to connect LoRa device to Domoticz
#
# Author: DiNy
#
#   Goal : 
#       - Log LoRa devices from Chirpstack App Server data into Domoticz
#
#   Concept : 
#       - ChirpStack is organized with Applications regrouping several Nodes. This plugin is ment to have one Hardware by Application ID.
#       - The LoRaWAN message use the Cayenne LPP format. Each Node can then have several channels.
#       - The user should declare the Application ID in the parameters of the Hardware 
#       - A MQTT listner will then start with topic application/ID/# 
#       - New devices will automatically be added to the hardware with a unique ID, and an incremented UNIT. Thus there is a max of 255 |node-channel-sensor| can be used.
#       - A unique device ID will be associated : "eui-[Chirpstack APPEUI]-[CayenneLPP-CHANNEL]-[SENSORTYPE]
#
#
#   TODO :
#       - Create merged sensor : temp+hum, temp+hum+baro into One sensor if associated to the same channel 
#       - Extend the Cayenne LPP possibilities by allowing the user to define its own decoding protocol ( CS_USER-Defined_to_DZ={} )
#       - Place the unsupported Cayenne LPP datatype into text sensors
#       - 
# 
# Credits : 
#   Uses the zigbee2mqtt domoticz plugin  https://github.com/stas-demydiuk/domoticz-zigbee2mqtt-plugin
#   Based on https://github.com/emontnemery/domoticz_mqtt_discovery
# Touched files : 
#   - plugin.py
#   - API/api.py
# License : MIT
"""
<plugin key="ChirpStack2Dz" name="Chirpstack MQTT to Domoticz" author="DiNy" version="0.0.2" externallink="https://github.com/Di-Ny/chirpstack2domoticz">
    <description>
        <h3>Chirpstack 2 Domoticz notice </h3><br/>
        A plugin to connect LoRa device to Domoticz.
        <br/>
        <b>Requirements:</b>
        <ul >
            <li>Already installed MQTT Server : https://www.domoticz.com/wiki/MQTT</li>
            <li>Working ChirpStack Application Server : https://www.chirpstack.io/</li>
            <li>A physical LoRa device configured to work on Chirpstack App Server, with <b>Cayenne LPP decoding</b></li>
            <li>For now only the following Cayenne LPP are supported : digital Input, Analog Input (0-255), illuminance, presence, temperature, humidity, barometer </li>
        </ul>
        <br/>
        <b>Description of parameters :</b><br/>
        <ul>
            <li>MQTT - Only tested on local hosted server, unencrypted. Port is filled by \"Connection\"</li>
            <li>Application ID - You find this in the ChirpStack Application Server. It will subscribe to the corresponding MQTT topic application/[ID]/#</li>
            <li>Automatically create new devices - Must be False to prevent the app adding new devices. Also Domoticz setting should allow new hardware</li>
            <li>Debug - Will display all MQTT data ofr the concerned Topic</li>
        </ul>
    </description>
    <params>
        <param field="Address" label="MQTT IP" width="200px" required="true" default="127.0.0.1"/>
        <param field="Port" label="Connection" required="true" width="200px">
            <options>
                <option label="Unencrypted" value="1883" default="true" />
                <option label="Encrypted (Client Certificate)" value="8883" />
            </options>
        </param>
        <param field="Username" label="MQTT Username (optional)" width="300px" required="false" default=""/>
        <param field="Password" label="MQTT Password (optional)" width="300px" required="false" default="" password="true"/>
        <param field="Mode3" label="MQTT Client ID (optional)" width="300px" required="false" default=""/>
        <param field="Mode1" label="Application ID" default="" required="false" width="200px"/>
        <param field="Mode2" label="Create devices" required="true" width="75px">
            <options>
                <option label="True" value="True" default="true"/>
                <option label="False" value="False"/>
            </options>
        </param>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="Verbose" value="Verbose"/>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal" default="true" />
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import json
import time
import re
import os
from shutil import copy2, rmtree
from mqtt import MqttClient
from api import API
import requests
# from devices_manager import DevicesManager
# from groups_manager impocdrt GroupsManager

from mqtt_globals import *

class BasePlugin:
    mqttClient = None

    def CS_2_DZ_decoder(self,topic, message):
        success = 0
        Domoticz.Debug("CS_Decoder")
        EUI = str(topic.split("device/")[1].split("/")[0])
        Domoticz.Debug("EUI : "+EUI)

        ############
        ## Devices
        payload = json.loads(message)
        Domoticz.Debug("Payload:\n"+str(payload))
        if not 'loRaSNR' in str(payload):
            Domoticz.Log("Decoding LoRa message problem. Check ChirpStack application.")
            return success
        RSSI=payload['rxInfo'][0]['loRaSNR']
        RSSI = int(round(mapFromTo(int(RSSI),-20,0,0,10), 0))#Domoticz : between 0 and 10
        Domoticz.Debug("RSSI : "+str(RSSI))
        # Domoticz.Debug("Objects:\n"+str(payload['object']))#{'temperatureSensor': {'1': 12}, 'humiditySensor': {'1': 80}}
        CS_objects = payload['object']
        if(len(CS_objects) == 0):
            Domoticz.Log("Decoding cayenne message problem. Check ChirpStack application.")
            return success
        # Domoticz.Debug(str(CS_objects))#{'temperatureSensor': {'1': 12}, 'humiditySensor': {'1': 80}}

        #Reorganize data 
        #Associate with the CS_cayenne_to_DZ table (mqtt_globals)
        data = []
        for obj in CS_objects :
            if str(obj) in CS_cayenne_to_DZ:
                for channel in CS_objects[str(obj)]:
                    #Get the value of the sensor 
                    value=str(CS_objects[str(obj)][str(channel)])
                    #build DATA : [Channel, value, [Corresp.DZ_TypeName   , Corresp.DZ_pType , DZ_sType, Corresp.FancyName, Corresp.UNIT_ID] ]
                    # Example: 	  ['1'    ,	'22' ,  ['Counter Incremental', 'Custom'		 , ...]] 
                    data.append([channel, value, CS_cayenne_to_DZ[str(obj)]])
            	#elseif (str(obj) in CS_payload_to_MS):
            else:
                Domoticz.Log("Unfound/Unproccessable Cayenne Data Type : "+str(obj))
        
        Domoticz.Debug("DATA structure:"+str(data))
        #[['1', '12', ['Temperature', 243, 17, 'temp']], ['2', '14', ['Temperature', 243, 17, 'temp']], ['3', '15', ['Temperature', 243, 17, 'temp']], ['1', '80', ['Humidity', 243, 3, 'hum']]]
        # #aggregate several sensor types into one sensor. Decide whi one is nvalue, which one is svalue
        # # TODO
        data_ag = data
        #Devices ID 
        d_ids=[]
        d_units=[]
        for x in Devices:
            d_ids.append([str(x),str(Devices[x].ID),str(Devices[x].Name),str(Devices[x].DeviceID)])
            d_units.append(int(x))
        Domoticz.Debug("d_ids:\n"+str(d_ids))
        Domoticz.Debug("d_units:\n"+str(d_units))

        #Device 
        for d in range(0,len(data_ag)):
            #   Case there is Type_Name assigned
            if data_ag[d][2][0] != "":
                #Shape the values 
                device_fancyname = str(data_ag[d][2][3])
                device_id="eui-"+EUI+"-"+str(data_ag[d][0])+"-"+device_fancyname#eui-a8d4fdf51239f322-1-hum
                device_Name="Unknown "+device_fancyname
                #Device type identification. Either there is a TypeName ("tn_") which is a shortcut for Type + Subtype + SwitchType, or theses 3 values are fullfilled
                device_TypeName=str(data_ag[d][2][0])
                device_Type=str(data_ag[d][2][1])
                device_Subtype=str(data_ag[d][2][2])
                #device_Switchtype=str(data_ag[d][2][0]) NOT IMPLEMENTED YET

                Domoticz.Debug("===================")
                Domoticz.Debug("device_id: "+str(device_id))
                #If not exist, create 
                if(device_id not in str(d_ids)):
                    #Find a new unit ID
                    device_Unit = 0
                    for u in range(1, 255):
                        if u not in d_units:
                            device_Unit = u
                            d_units.append(u)
                            break
                    if device_Unit == 0:
                        Domoticz.Log("ERROR - No more UNIT ID to allocate. Device not created")
                        return 0
                    Domoticz.Debug("device_Name: "+str(device_Name))
                    Domoticz.Debug("device_TypeName: "+str(device_TypeName))
                    Domoticz.Debug("device_Type: "+str(device_Type))
                    Domoticz.Debug("device_Subtype: "+str(device_Subtype))
                    if self.create_new_devices == "True":
                        Domoticz.Log("ChirpStack Plugin - Create NEW device with ID="+str(device_id)+", Name="+str(device_Name)+", Type="+str(device_TypeName))
                        #Create. 
                        if device_TypeName == tn_null:
                            #Create device with Type + Subtype.
                            Domoticz.Device(Name=device_Name, Type=device_Type, Subtype=device_Subtype, Unit=device_Unit, DeviceID=device_id).Create()
                        else:
                            #Can only create Type Names (tn_) known by Domoticz.
                            Domoticz.Device(Name=device_Name, TypeName=device_TypeName, Unit=device_Unit, DeviceID=device_id).Create()
                    else:
                        Domoticz.Log("ChirpStack Plugin - DISBALED [Create device "+str(device_id)+"]")
                for x in Devices:
                    #Check if now exists, and update 
                    if(str(Devices[x].DeviceID) == device_id):
                        device_svalue = str(data_ag[d][1])
                        device_nvalue = 0
                        #Update
                        Domoticz.Log("Chirpstack Plugin - Update device (ID="+str(Devices[x].ID)+") value ="+data_ag[d][1])
                        
                        #Check if a float should be sent instead of an integer
                        # if "." in device_svalue or ";" in device_svalue :
                        #     device_nvalue = 0
                        # else:
                        #     device_nvalue = int(float(device_svalue))
                        #     device_svalue = 0
                        
                        #Handle specific cases 
                        #       RAIN
                        #       GPS
                        
                        Devices[x].Update(nValue=device_nvalue, sValue=str(device_svalue), SignalLevel=RSSI)
                Domoticz.Debug("===================")
        return success

    def onStart(self):
        self.debugging = Parameters["Mode6"]
        if self.debugging == "Verbose":
            Domoticz.Debugging(2+4+8+16+64)
        if self.debugging == "Debug":
            Domoticz.Debugging(2)
        DumpConfigToLog()
        Domoticz.Log("Chirpstack2Domoticz Plugin started")
        #App ID Base TOPIC
        if(Parameters["Mode1"].strip() != ""):
            self.base_topic = "application/"+Parameters["Mode1"].strip()
        else:
            Domoticz.Log("Warning : No Application ID submitted. It will subscribe to all application topics")
            self.base_topic = "application"
        self.subscribed_for_devices = False
        self.create_new_devices = Parameters["Mode2"].strip()
        mqtt_server_address = Parameters["Address"].strip()
        mqtt_server_port = Parameters["Port"].strip()
        mqtt_client_id = Parameters["Mode3"].strip()

        self.mqttClient = MqttClient(mqtt_server_address, mqtt_server_port, mqtt_client_id, self.onMQTTConnected, self.onMQTTDisconnected, self.onMQTTPublish, self.onMQTTSubscribed)
        self.api = API(Devices, self.publishToMqtt)

    def checkDevices(self):
        Domoticz.Debug("checkDevices called")

    def onStop(self):
        Domoticz.Debug("onStop called")
        #self.uninstall()


    def onCommand(self, Unit, Command, Level, Color):
        Domoticz.Debug("onCommand: " + Command + ", level (" + str(Level) + ") Color:" + Color)

        message = None
        device = Devices[Unit] #Devices is Domoticz collection of devices for this hardware
        device_params = device.DeviceID.split('_')
        entity_id = device_params[0]
        Domoticz.Debug("OnCommand --> Partie desctivee")
        # if (self.devices_manager.get_device_by_id(entity_id) != None):
        #     message = self.devices_manager.handle_command(Devices, device, Command, Level, Color)
        # elif(self.groups_manager.get_group_by_deviceid(device.DeviceID) != None):
        #     message = self.groups_manager.handle_command(device, Command, Level, Color)
        # else:
        #     Domoticz.Log('Can\'t process command from device "' + device.Name + '"')

        # if (message != None):
        #     self.publishToMqtt(message['topic'], message['payload'])

    def publishToMqtt(self, topic, payload):
        self.mqttClient.publish(self.base_topic + '/' + topic, payload)

    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug("onConnect called")
        self.mqttClient.onConnect(Connection, Status, Description)

    def onDisconnect(self, Connection):
        self.mqttClient.onDisconnect(Connection)

    def onDeviceModified(self, unit):
        if (unit == 255):
            self.api.handle_request(Devices[unit].sValue)
            return

    def onMessage(self, Connection, Data):
        self.mqttClient.onMessage(Connection, Data)

    def onHeartbeat(self):
        self.mqttClient.onHeartbeat()

    def onMQTTConnected(self):
        #if connected subscirbe to topic 
        self.mqttClient.subscribe([self.base_topic+"/#"])
        Domoticz.Log("MQTT subscribed to : "+self.base_topic+"/#")

    def onMQTTDisconnected(self):
        self.subscribed_for_devices = False

    def onMQTTSubscribed(self):
        Domoticz.Debug("onMQTTSubscribed")

    def onMQTTPublish(self, topic, message):
        Domoticz.Debug("On MQTT Publish")
        payload = json.dumps(message)
        Domoticz.Debug("MQTT message: " + topic + " " + str(payload))
        topic = topic.replace(self.base_topic + '/', '')
        #self.api.handle_mqtt_message(topic, message)
        #Decode the pyaload and message. --> Will automatically add sensors
        self.CS_2_DZ_decoder(topic, payload)

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return

def DumpDictionaryToLog(theDict, Depth=""):
    if isinstance(theDict, dict):
        for x in theDict:
            if isinstance(theDict[x], dict):
                Domoticz.Log(Depth+"> Dict '"+x+"' ("+str(len(theDict[x]))+"):")
                DumpDictionaryToLog(theDict[x], Depth+"---")
            elif isinstance(theDict[x], list):
                Domoticz.Log(Depth+"> List '"+x+"' ("+str(len(theDict[x]))+"):")
                DumpListToLog(theDict[x], Depth+"---")
            elif isinstance(theDict[x], str):
                Domoticz.Log(Depth+">'" + x + "':'" + str(theDict[x]) + "'")
            else:
                Domoticz.Log(Depth+">'" + x + "': " + str(theDict[x]))

def DumpListToLog(theList, Depth):
    if isinstance(theList, list):
        for x in theList:
            if isinstance(x, dict):
                Domoticz.Log(Depth+"> Dict ("+str(len(x))+"):")
                DumpDictionaryToLog(x, Depth+"---")
            elif isinstance(x, list):
                Domoticz.Log(Depth+"> List ("+str(len(theList))+"):")
                DumpListToLog(x, Depth+"---")
            elif isinstance(x, str):
                Domoticz.Log(Depth+">'" + x + "':'" + str(theList[x]) + "'")
            else:
                Domoticz.Log(Depth+">'" + x + "': " + str(theList[x]))

def mapFromTo(x,a,b,c,d):
    #
    if a <b :
        if x < a:
            x=a
        if x > b :
            x=b
    else:
        if x > a:
            x=a
        if x <b:
            x=b

    y=(x-a)/(b-a)*(d-c)+c
    return y
