# chirpstack2domoticz
Domoticz plugin to intergrate data coming from chirpstack application server
### Goal : 
- Log LoRa devices from Chirpstack App Server data into Domoticz
### Concept : 
- ChirpStack is organized with Applications regrouping several Nodes. This plugin is ment to have one Hardware by Application ID.
- The LoRaWAN message use the Cayenne LPP format. Each Node can then have several channels.
- The user should declare the Application ID in the parameters of the Hardware 
- A MQTT listner will then start with topic application/ID/ 
- New devices will automatically be added to the hardware with a unique ID, and an incremented UNIT. Thus there is a max of 255 |node-channel-sensor| can be used.
- A unique device ID will be associated : "eui-[Chirpstack APPEUI]-[CayenneLPP-CHANNEL]-[SENSORTYPE]

### TODO :
- [] Create merged sensor : temp+hum, temp+hum+baro into One sensor if associated to the same channel 
- [] Extend the Cayenne LPP possibilities by allowing the user to define its own decoding protocol ( CS_USER-Defined_to_DZ={} )
- [] Place the unsupported Cayenne LPP datatype into text sensors
 
Credits : 
Made from the [zigbee2mqtt domoticz plugin](https://github.com/stas-demydiuk/domoticz-zigbee2mqtt-plugin) based on [domoticz_mqtt_discovery](https://github.com/emontnemery/domoticz_mqtt_discovery)

License : MIT


Touched files : 
   - plugin.py
   - API/api.py

 
# Installation 

### Requirements

- Installed [MQTT Server](https://www.domoticz.com/wiki/MQTT)
- Working [ChirpStack Application Server](https://www.chirpstack.io/)
- A physical LoRa device configured to work on Chirpstack App Server (it used a LoPy4 from Pycom)
- Cayenne LPP encoding. For now only the following Cayenne LPP are supported : digital Input, Analog Input (0-255), illuminance, presence, temperature, humidity, barometer 
 
### Installation 

See [Using_Python_plugins](https://www.domoticz.com/wiki/Using_Python_plugins)

0. Go to your ChirpStack application server. Copy the **ID of the application**, its Name, the MQTT server address Chirpstack publishes onto. 
1. Clone repository into domoticz/plugins

> cd domoticz/plugins
>
> git clone https://github.com/Di-Ny/chirpstack2domoticz

2. Restart Domoticz
3. Domoticz > Settings : "Accept new Hardware Devices"
4. Domoticz > Hardware > Find in the list "Chirpstack MQTT to Domoticz". Name it like the ChirpStack Application, you want to copy the devices from. 
5. Fill in the parameters your saved from Chirpstack
6. Click "Add"

# Usage example
Plugin Setup

![Plugin Setup](/images/Domoticz_plugin.JPG)

Receive sensor data on ChirpStack 

![CS](/images/Chirpstackserver_device.JPG)

![CS Sensor Data](/images/Chirpstackserver.JPG)


On the Domoticz Log, new sensors are found and added automatically : 

![DZ Log](/images/Domoticz.Log.JPG)

![DZ Devices](/images/Domoticz_devices.JPG)
