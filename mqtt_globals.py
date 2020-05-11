# mqtt_globals.py
# Author: Nicolas DAUY
#
#   Goal : 
#       - Simple file to load mqtt constants and pair them with different systems
#	Contains : 
#		- MySensors constants
#		- Chirpsack constants
#		- Domoticz constants
#		- Association json arrays

#############
##	GLOBAL
#CONFIGURATION - Unused in Domoticz
SERVEUR='127.0.0.1'
PORT=1883

#############
##	MYSENSORS
#MyMQTT.=Defaults=MySensors=values=in=mqtt_globals.py.=See=https://www.mysensors.org/download/serial_api_20
NODE_ID_VOLTAGE=		10
NODE_ID_AMBIANT=		11
NODE_ID_ALERT=			12
NODE_ID_CHIRPSTACK=		200

	#sensorsType=-->=presentation
S_DOOR	=			0	#Door=and=window=sensors	V_TRIPPED,=V_ARMED
S_MOTION	=		1	#Motion=sensors	V_TRIPPED,=V_ARMED
S_SMOKE	=			2	#Smoke=sensor	V_TRIPPED,=V_ARMED
S_BINARY	=		3	#Binary=device=(on/off)	V_STATUS,=V_WATT
S_DIMMER	=		4	#Dimmable=device=of=some=kind	V_STATUS=(on/off),=V_PERCENTAGE=(dimmer=level=0-100),=V_WATT
S_COVER	=			5	#Window=covers=or=shades	V_UP,=V_DOWN,=V_STOP,=V_PERCENTAGE
S_TEMP	=			6	#Temperature=sensor	V_TEMP,=V_ID
S_HUM	=			7	#Humidity=sensor	V_HUM
S_BARO	=			8	#Barometer=sensor=(Pressure)	V_PRESSURE,=V_FORECAST
S_WIND	=			9	#Wind=sensor	V_WIND,=V_GUST,=V_DIRECTION
S_RAIN	=			10	#Rain=sensor	V_RAIN,=V_RAINRATE
S_UV	=			11	#UV=sensor	V_UV
S_WEIGHT	=		12	#Weight=sensor=for=scales=etc.	V_WEIGHT,=V_IMPEDANCE
S_POWER	=			13	#Power=measuring=device,=like=power=meters	V_WATT,=V_KWH,=V_VAR,=V_VA,=V_POWER_FACTOR
S_HEATER	=		14	#Heater=device	V_HVAC_SETPOINT_HEAT,=V_HVAC_FLOW_STATE,=V_TEMP,=V_STATUS
S_DISTANCE	=		15	#Distance=sensor	V_DISTANCE,=V_UNIT_PREFIX
S_LIGHT_LEVEL=		16	#Light=sensor	V_LIGHT_LEVEL=(uncalibrated=percentage),=V_LEVEL=(light=level=in=lux)
S_ARDUINO_NOD=		17	#Arduino=node=device
S_ARDUINO_REPEATER_NODE	=18	#Arduino=repeating=node=device
S_LOCK	=			19	#Lock=device	V_LOCK_STATUS
S_IR	=			20	#Ir=sender/receiver=device	V_IR_SEND,=V_IR_RECEIVE,=V_IR_RECORD
S_WATER	=			21	#Water=meter	V_FLOW,=V_VOLUME
S_AIR_QUALITY=		22	#Air=quality=sensor=e.g.=MQ-2	V_LEVEL,=V_UNIT_PREFIX
S_CUSTOM	=		23	#Use=this=for=custom=sensors=where=no=other=fits.
S_DUST	=			24	#Dust=level=sensor	V_LEVEL,=V_UNIT_PREFIX
S_SCENE_CONTROLLER=	25	#Scene=controller=device	V_SCENE_ON,=V_SCENE_OFF
S_RGB_LIGHT	=		26	#RGB=light	V_RGB,=V_WATT
S_RGBW_LIGHT	=	27	#RGBW=light=(with=separate=white=component)	V_RGBW,=V_WATT
S_COLOR_SENSOR	=	28	#Color=sensor	V_RGB
S_HVAC	=			29	#Thermostat/HVAC=device	V_STATUS,=V_TEMP,=V_HVAC_SETPOINT_HEAT,=V_HVAC_SETPOINT_COOL,=V_HVAC_FLOW_STATE,=V_HVAC_FLOW_MODE,=V_HVAC_SPEED
S_MULTIMETER	=	30	#Multimeter=device	V_VOLTAGE,=V_CURRENT,=V_IMPEDANCE
S_SPRINKLER	=		31	#Sprinkler=device	V_STATUS=(turn=on/off),=V_TRIPPED=(if=fire=detecting=device)
S_WATER_LEAK	=	32	#Water=leak=sensor	V_TRIPPED,=V_ARMED
S_SOUND	=			33	#Sound=sensor	V_LEVEL=(in=dB),=V_TRIPPED,=V_ARMED
S_VIBRATION	=		34	#Vibration=sensor	V_LEVEL=(vibration=in=Hz),=V_TRIPPED,=V_ARMED
S_MOISTURE	=		35	#Moisture=sensor	V_LEVEL=(water=content=or=moisture=in=percentage?),=V_TRIPPED,=V_ARMED
S_INFO	=			36	#LCD=text=device	V_TEXT
S_GAS	=			37	#Gas=meter	V_FLOW,=V_VOLUME
S_GPS	=			38	#GPS=Sensor	V_POSITION
S_WATER_QUALITY	=	39	#Water=quality=sensor	V_TEMP,=V_PH,=V_ORP,=V_EC,=V_STATUS

	#Command=
C_presentation=		0	#Sent=by=a=node=when=they=present=attached=sensors.=This=is=usually=done=in=the=presentation()=function=which=runs=at=startup.
C_set=				1	#This=message=is=sent=from=or=to=a=sensor=when=a=sensor=value=should=be=updated
C_req=				2	#Requests=a=variable=value=(usually=from=an=actuator=destined=for=controller).
C_internal=			3	#This=is=a=special=internal=message.=See=table=below=for=the=details
C_stream=			4	#Used=for=OTA=firmware=updates

	#Type=-->=set,=request
V_TEMP=				0	#Temperature	S_TEMP,=S_HEATER,=S_HVAC,=S_WATER_QUALITY
V_HUM=				1	#Humidity	S_HUM
V_STATUS=			2	#Binary=status.=0=off=1=on	S_BINARY,=S_DIMMER,=S_SPRINKLER,=S_HVAC,=S_HEATER,=S_WATER_QUALITY
V_PERCENTAGE=		3	#Percentage=value.=0-100=(%)	S_DIMMER,=S_COVER
V_PRESSURE=			4	#Atmospheric=Pressure	S_BARO
V_FORECAST=			5	#Whether=forecast.=One=of="stable",="sunny",="cloudy",="unstable",="thunderstorm"=or="unknown"	S_BARO
V_RAIN=				6	#Amount=of=rain	S_RAIN
V_RAINRATE=			7	#Rate=of=rain	S_RAIN
V_WIND=				8	#Windspeed	S_WIND
V_GUST=				9	#Gust	S_WIND
V_DIRECTION=		10	#Wind=direction=0-360=(degrees)	S_WIND
V_UV=				11	#UV=light=level	S_UV
V_WEIGHT=			12	#Weight=(for=scales=etc)	S_WEIGHT
V_DISTANCE=			13	#Distance	S_DISTANCE
V_IMPEDANCE=		14	#Impedance=value	S_MULTIMETER,=S_WEIGHT
V_ARMED=			15	#Armed=status=of=a=security=sensor.=1=Armed,=0=Bypassed	S_DOOR,=S_MOTION,=S_SMOKE,=S_SPRINKLER,=S_WATER_LEAK,=S_SOUND,=S_VIBRATION,=S_MOISTURE
V_TRIPPED=			16	#Tripped=status=of=a=security=sensor.=1=Tripped,=0=Untripped	S_DOOR,=S_MOTION,=S_SMOKE,=S_SPRINKLER,=S_WATER_LEAK,=S_SOUND,=S_VIBRATION,=S_MOISTURE
V_WATT=				17	#Watt=value=for=power=meters	S_POWER,=S_BINARY,=S_DIMMER,=S_RGB_LIGHT,=S_RGBW_LIGHT
V_KWH=				18	#Accumulated=number=of=KWH=for=a=power=meter	S_POWER
V_SCENE_ON=			19	#Turn=on=a=scene	S_SCENE_CONTROLLER
V_SCENE_OFF=		20	#Turn=of=a=scene	S_SCENE_CONTROLLER
V_HVAC_FLOW_STATE=	21	#Mode=of=header.=One=of="Off",="HeatOn",="CoolOn",=or="AutoChangeOver"	S_HVAC,=S_HEATER
V_HVAC_SPEED=		22	#HVAC/Heater=fan=speed=("Min",="Normal",="Max",="Auto")	S_HVAC,=S_HEATER
V_LIGHT_LEVEL=		23	#Uncalibrated=light=level.=0-100%.=Use=V_LEVEL=for=light=level=in=lux.	S_LIGHT_LEVEL
V_VAR1=				24	#Custom=value	Any=device
V_VAR2=				25	#Custom=value	Any=device
V_VAR3=				26	#Custom=value	Any=device
V_VAR4=				27	##Custom=value	Any=device
V_VAR5=				28	#Custom=value	Any=device
V_UP=				29	#Window=covering.=Up.	S_COVER
V_DOWN=				30	#Window=covering.=Down.	S_COVER
V_STOP=				31	#Window=covering.=Stop.	S_COVER
V_IR_SEND=			32	#Send=out=an=IR-command	S_IR
V_IR_RECEIVE=		33	#This=message=contains=a=received=IR-command	S_IR
V_FLOW=				34	#Flow=of=water/gas=(in=meter)	S_WATER,=S_GAS
V_VOLUME=			35	#Water/gas=volume	S_WATER,=S_GAS
V_LOCK_STATUS=		36	#Set=or=get=lock=status.=1=Locked,=0=Unlocked	S_LOCK
V_LEVEL=			37	#Used=for=sending=level-value	S_DUST,=S_AIR_QUALITY,=S_SOUND=(dB),=S_VIBRATION=(hz),=S_LIGHT_LEVEL=(lux)
V_VOLTAGE=			38	#Voltage=level	S_MULTIMETER
V_CURRENT=			39	#Current=level	S_MULTIMETER
V_RGB=				40	#RGB=value=transmitted=as=ASCII=hex=string=(I.e="ff0000"=for=red)	S_RGB_LIGHT,=S_COLOR_SENSOR
V_RGBW=				41	#RGBW=value=transmitted=as=ASCII=hex=string=(I.e="ff0000ff"=for=red=+=full=white)	S_RGBW_LIGHT
V_ID=				42	#Optional=unique=sensor=id=(e.g.=OneWire=DS1820b=ids)	S_TEMP
V_UNIT_PREFIX=		43	#Allows=sensors=to=send=in=a=string=representing=the=unit=prefix=to=be=displayed=in=GUI.=This=is=not=parsed=by=controller!=E.g.=cm,=m,=km,=inch.	S_DISTANCE,=S_DUST,=S_AIR_QUALITY
V_HVAC_SETPOINT_COOL=44	#HVAC=cold=setpoint	S_HVAC
V_HVAC_SETPOINT_HEAT=45	#HVAC/Heater=setpoint	S_HVAC,=S_HEATER
V_HVAC_FLOW_MODE=	46	#Flow=mode=for=HVAC=("Auto",="ContinuousOn",="PeriodicOn")	S_HVAC
V_TEXT=				47	#Text=message=to=display=on=LCD=or=controller=device	S_INFO
V_CUSTOM=			48	#Custom=messages=used=for=controller/inter=node=specific=commands,=preferably=using=S_CUSTOM=device=type.	S_CUSTOM
V_POSITION=			49	#GPS=position=and=altitude.=Payload:=latitude;longitude;altitude(m).=E.g.="55.722526;13.017972;18"	S_GPS
V_IR_RECORD=		50	#Record=IR=codes=S_IR=for=playback	S_IR
V_PH=				51	#Water=PH	S_WATER_QUALITY
V_ORP=				52	#Water=ORP=:=redox=potential=in=mV	S_WATER_QUALITY
V_EC=				53	#Water=electric=conductivity=μS/cm=(microSiemens/cm)	S_WATER_QUALITY
V_VAR=				54	#Reactive=power:=volt-ampere=reactive=(var)	S_POWER
V_VA=				55	#Apparent=power:=volt-ampere=(VA)	S_POWER
V_POWER_FACTOR=		56	#Ratio=of=real=power=to=apparent=power:=floating=point=value=in=the=range=[-1,..,1]	S_POWER

#############
##= DOMOTICZ
#  https://github.com/domoticz/domoticz/blob/development/hardware/hardwaretypes.h
pTypeLux=							0xF6
sTypeLux=							0x01

pTypeTEMP_BARO=						0xF7
sTypeBMP085=						0x01

pTypeUsage=							0xF8
sTypeElectric=						0x01

pTypeAirQuality=					0xF9
sTypeVoltcraft=						0x01

pTypeP1Power=						0xFA
sTypeP1Power=						0x01
mModeP1Norm=						0x00
mModeP1Double=						0x01

pTypeP1Gas=							0xFB
sTypeP1Gas=							0x02

pTypeYouLess=						0xFC
sTypeYouLess=						0x01

pTypeRego6XXTemp=					0xFD
sTypeRego6XXTemp=					0x01

pTypeRego6XXValue=					0xFE
sTypeRego6XXStatus=					0x02
sTypeRego6XXCounter=				0x03

sTypeRFY2=							0xFE
pTypeEvohome=						0x45
sTypeEvohome=						0x00#Controller
pTypeEvohomeZone=					0x46#Seems=easier=to=define=a=new=type=here
sTypeEvohomeZone=					0x00#Actual=temp=zone
pTypeEvohomeWater=					0x47#Seems=easier=to=define=a=new=type=here
sTypeEvohomeWater=					0x00#Hot=water=(Ideally=this=would=just=be=a=zone=but=for=whatever=reason=evohome=treats=this=differently)
pTypeEvohomeRelay=					0x44#Relay
sTypeEvohomeRelay=					0x00
#general
pTypeGeneral=						0xF3
sTypeVisibility=					0x01
sTypeSolarRadiation=				0x02
sTypeSoilMoisture=					0x03
sTypeLeafWetness=					0x04
sTypeSystemTemp=					0x05
sTypePercentage=					0x06
sTypeFan=							0x07
sTypeVoltage=						0x08
sTypePressure=						0x09
sTypeSetPoint=						0x10
sTypeTemperature=					0x11
sTypeZWaveClock=					0x12
sTypeTextStatus=					0x13
sTypeZWaveThermostatMode=			0x14
sTypeZWaveThermostatFanMode=		0x15
sTypeAlert=							0x16
sTypeCurrent=						0x17
sTypeSoundLevel=					0x18
sTypeUV=							0x19
sTypeBaro=							0x1A
sTypeDistance=						0x1B
sTypeCounterIncremental=			0x1C
sTypeKwh=							0x1D
sTypeWaterflow=						0x1E
sTypeCustom=						0x1F
sTypeZWaveAlarm=					0x20
sTypeManagedCounter=				0x21
sTypeZWaveThermostatOperatingState= 0x23

pTypeGeneralSwitch=					0xF4
sSwitchCustomSwitch=				0x48
sSwitchGeneralSwitch=				0x49

#TypeName
tn_null=""
tn_airquality="Air Quality"
tn_alert="Alert"
tn_baro ="Barometer"
tn_counter_incr ="Counter Incremental"
tn_contact ="Contact"
tn_current_amp ="Current/Ampere"
tn_current_sing ="Current (Single)"
tn_custom ="Custom"
tn_dim ="Dimmer"
tn_dist ="Distance"
tn_gas ="Gas"
tn_hum ="Humidity"
tn_lux ="Illumination"
tn_kwh ="kWh"
tn_leaf_wet ="Leaf Wetness"
tn_motion ="Motion"
tn_percent ="Percentage"
tn_pushon ="Push On"
tn_pushoff ="Push Off"
tn_pressure ="Pressure"
tn_rain ="Rain"
tn_sel_switch ="Selector Switch"
tn_soil_moist ="Soil Moisture"
tn_solar_rad ="Solar Radiation"
tn_soundlevel ="Sound Level"
tn_switch ="Switch"
tn_temp ="Temperature"
tn_temphum ="Temp+Hum"
tn_temphumbaro ="Temp+Hum+Baro"
tn_text ="Text"
tn_usage ="Usage"
tn_UV ="UV"
tn_visibility ="Visibility"
tn_volt ="Voltage"
tn_waterflow ="Waterflow"
tn_wind ="Wind"
tn_windtempchill ="Wind+Temp+Chill"


#############
##	CHIRPSTACK
##See=Github=>=chirpstack-application-server/internal/codec/cayennelpp/cayennelpp.go
topic_cs_app='application/#'	#unused in Domoticz
CS_EUI_POS=3
CS_digitalInput="digitalInput"
CS_digitalOutput="digitalOutput"
CS_analogInput="analogInput"
CS_analogOutput="analogOutput"
CS_illuminanceSensor="illuminanceSensor"
CS_presenceSensor="presenceSensor"
CS_temperatureSensor="temperatureSensor"
CS_humiditySensor="humiditySensor"
CS_accelerometer="accelerometer"
CS_barometer="barometer"
CS_gyrometer="gyrometer"
CS_gps_location="gps_location"

#############
##	ASSOCIATION ARRAYS
#CS_cayenne_to_MS[Name=in=the=Chirpstack=App=Server]===[MYSENSORS_SensorType,=MYSENSORS_Type]
CS_cayenne_to_MS={
	CS_digitalInput:[S_BINARY,V_STATUS],
	CS_digitalOutput:[S_BINARY,V_STATUS],
	CS_analogInput:[S_CUSTOM,V_LEVEL],
	CS_analogOutput:[S_CUSTOM,V_LEVEL],
	CS_illuminanceSensor:[S_LIGHT_LEVEL,V_LIGHT_LEVEL],
	CS_presenceSensor:[S_MOTION,V_TRIPPED],
	CS_temperatureSensor:[S_TEMP,V_TEMP],
	CS_humiditySensor:[S_HUM,V_HUM],
	CS_accelerometer:[S_BINARY,V_STATUS],
	CS_barometer:[S_BARO,V_PRESSURE],
	CS_gyrometer:[S_BINARY,V_STATUS],
	CS_gps_location:[S_GPS,V_POSITION]
}

## To DZ values format :  "ChirpStack-CAYENNE":[DZ_TypeName, DZ_pType,DZ_sType, FancyName, UNIT_ID]
CS_cayenne_to_DZ={
	CS_digitalInput:[tn_contact, pTypeGeneral,sTypeCustom,"digital"],
	CS_analogInput:[tn_custom, pTypeGeneral,sTypeCustom,"analog"],
	CS_illuminanceSensor:[tn_lux, pTypeLux,sTypeLux,"lux"],
	CS_presenceSensor:[tn_motion, pTypeGeneralSwitch,sSwitchGeneralSwitch,"motion"],
	CS_temperatureSensor:[tn_temp, pTypeGeneral,sTypeTemperature,"temp"],
	CS_humiditySensor:[tn_hum,pTypeGeneral,sTypeSoilMoisture,"hum"],
	CS_barometer:[tn_baro,pTypeGeneral,sTypeBaro,"baro"]
}
