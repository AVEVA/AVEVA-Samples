# program.py
#
# Copyright (C) 2018 OSIsoft, LLC. All rights reserved.
#
# THIS SOFTWARE CONTAINS CONFIDENTIAL INFORMATION AND TRADE SECRETS OF
# OSIsoft, LLC.  USE, DISCLOSURE, OR REPRODUCTION IS PROHIBITED WITHOUT
# RESTRICTED RIGHTS LEGEND
# Use, duplication, or disclosure by the Government is subject to restrictions
# as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and
# Computer Software clause at DFARS 252.227.7013
#
# OSIsoft, LLC
# 1600 Alvarado St, San Leandro, CA 94577

from sdspy import *
import configparser
import datetime
import time
import math
import inspect
import collections

#returns a type that represents the WaveData data
def getWaveDataType(sampleTypeId):
    if sampleTypeId is None or not isinstance(sampleTypeId, str):
        raise TypeError("sampleTypeId is not an instantiated string")

    intType = SdsType()
    intType.Id = "intType"
    intType.SdsTypeCode = SdsTypeCode.Int32

    doubleType = SdsType()
    doubleType.Id = "doubleType"
    doubleType.SdsTypeCode = SdsTypeCode.Double

    # note that the Order is the key (primary index)
    orderProperty = SdsTypeProperty()
    orderProperty.Id = "Order"
    orderProperty.SdsType = intType
    orderProperty.IsKey = True

    tauProperty = SdsTypeProperty()
    tauProperty.Id = "Tau"
    tauProperty.SdsType = doubleType

    radiansProperty = SdsTypeProperty()
    radiansProperty.Id = "Radians"
    radiansProperty.SdsType = doubleType

    sinProperty = SdsTypeProperty()
    sinProperty.Id = "Sin"
    sinProperty.SdsType = doubleType

    cosProperty = SdsTypeProperty()
    cosProperty.Id = "Cos"
    cosProperty.SdsType = doubleType

    tanProperty = SdsTypeProperty()
    tanProperty.Id = "Tan"
    tanProperty.SdsType = doubleType

    sinhProperty = SdsTypeProperty()
    sinhProperty.Id = "Sinh"
    sinhProperty.SdsType = doubleType

    coshProperty = SdsTypeProperty()
    coshProperty.Id = "Cosh"
    coshProperty.SdsType = doubleType

    tanhProperty = SdsTypeProperty()
    tanhProperty.Id = "Tanh"
    tanhProperty.SdsType = doubleType

    #create an SdsType for WaveData Class
    wave = SdsType()
    wave.Id = sampleTypeId
    wave.Name = "WaveDataSample"
    wave.Description = "This is a sample Sds type for storing WaveData type events"
    wave.SdsTypeCode = SdsTypeCode.Object
    wave.Properties = [orderProperty, tauProperty, radiansProperty, sinProperty, 
                       cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty]

    return wave
#returns a type that represents the WaveDataTarget data
def getWaveDataTargetType(sampleTypeId):
    if sampleTypeId is None or not isinstance(sampleTypeId, str):
        raise TypeError("sampleTypeId is not an instantiated string")

    intType = SdsType()
    intType.Id = "intType"
    intType.SdsTypeCode = SdsTypeCode.Int32

    doubleType = SdsType()
    doubleType.Id = "doubleType"
    doubleType.SdsTypeCode = SdsTypeCode.Double

    # note that the Order is the key (primary index)
    orderTargetProperty = SdsTypeProperty()
    orderTargetProperty.Id = "OrderTarget"
    orderTargetProperty.SdsType = intType
    orderTargetProperty.IsKey = True

    tauTargetProperty = SdsTypeProperty()
    tauTargetProperty.Id = "TauTarget"
    tauTargetProperty.SdsType = doubleType

    radiansTargetProperty = SdsTypeProperty()
    radiansTargetProperty.Id = "RadiansTarget"
    radiansTargetProperty.SdsType = doubleType

    sinTargetProperty = SdsTypeProperty()
    sinTargetProperty.Id = "SinTarget"
    sinTargetProperty.SdsType = doubleType

    cosTargetProperty = SdsTypeProperty()
    cosTargetProperty.Id = "CosTarget"
    cosTargetProperty.SdsType = doubleType

    tanTargetProperty = SdsTypeProperty()
    tanTargetProperty.Id = "TanTarget"
    tanTargetProperty.SdsType = doubleType

    sinhTargetProperty = SdsTypeProperty()
    sinhTargetProperty.Id = "SinhTarget"
    sinhTargetProperty.SdsType = doubleType

    coshTargetProperty = SdsTypeProperty()
    coshTargetProperty.Id = "CoshTarget"
    coshTargetProperty.SdsType = doubleType

    tanhTargetProperty = SdsTypeProperty()
    tanhTargetProperty.Id = "TanhTarget"
    tanhTargetProperty.SdsType = doubleType

    #create an SdsType for WaveData Class
    wave = SdsType()
    wave.Id = sampleTargetTypeId
    wave.Name = "WaveDataTargetSample"
    wave.Description = "This is a sample Sds type for storing WaveDataTarget type events"
    wave.SdsTypeCode = SdsTypeCode.Object
    wave.Properties = [orderTargetProperty, tauTargetProperty, radiansTargetProperty, sinTargetProperty, 
                       cosTargetProperty, tanTargetProperty, sinhTargetProperty, coshTargetProperty, tanhTargetProperty]

    return wave

#returns a type that represents WaveDataInteger data
def getWaveDataIntegerType(sampleTypeId):
    if sampleTypeId is None or not isinstance(sampleTypeId, str):
        raise TypeError("sampleTypeId is not an instantiated string")

    intType = SdsType()
    intType.Id = "intType"
    intType.SdsTypeCode = SdsTypeCode.Int32

    # note that the Order is the key (primary index)
    orderTargetProperty = SdsTypeProperty()
    orderTargetProperty.Id = "OrderTarget"
    orderTargetProperty.SdsType = intType
    orderTargetProperty.IsKey = True

    sinIntProperty = SdsTypeProperty()
    sinIntProperty.Id = "SinInt"
    sinIntProperty.SdsType = intType

    cosIntProperty = SdsTypeProperty()
    cosIntProperty.Id = "CosInt"
    cosIntProperty.SdsType = intType

    tanIntProperty = SdsTypeProperty()
    tanIntProperty.Id = "TanInt"
    tanIntProperty.SdsType = intType

    #create an SdsType for the WaveDataInteger Class
    wave = SdsType()
    wave.Id = sampleIntegerTypeId
    wave.Name = "WaveDataIntegerSample"
    wave.Description = "This is a sample Sds type for storing WaveDataInteger type events"
    wave.SdsTypeCode = SdsTypeCode.Object
    wave.Properties = [orderTargetProperty, sinIntProperty, 
                       cosIntProperty, tanIntProperty]

    return wave

# Generate a new WaveData event
def nextWave(now, interval, multiplier, order):
    totalSecondsDay = (now - now.replace(hour=0, minute=0, second = 0, microsecond = 0)).total_seconds() * 1000
    intervalSeconds = (interval - interval.replace(hour=0, minute=0, second = 0, microsecond = 0)).total_seconds() * 1000
    radians = ((totalSecondsDay % intervalSeconds ) / intervalSeconds) * 2 * math.pi
        
    newWave = WaveData()
    newWave.Order = order
    newWave.Radians = radians
    newWave.Tau = radians / (2 * math.pi)
    newWave.Sin = multiplier * math.sin(radians)
    newWave.Cos = multiplier * math.cos(radians)
    newWave.Tan = multiplier * math.tan(radians)
    newWave.Sinh = multiplier * math.sinh(radians)
    newWave.Cosh = multiplier * math.cosh(radians)
    newWave.Tanh = multiplier * math.tanh(radians)
        
    return newWave

# we'll use the following for cleanup, supressing errors
def supressError(sdsCall):
    try:
        sdsCall()
    except Exception as e:
        print(("Encountered Error: {error}".format(error = e)))

def isprop(v):
  return isinstance(v, property)

def toString(event):
    string = ""

    props = inspect.getmembers(WaveData,
                                    lambda o: isinstance(o, property))

    printOrder = [2,3,4,0,6,5,1,7,8]
    orderedProps = [props[i] for i in printOrder]
    for prop in orderedProps:
        value = getattr(event, prop[0])
        if value is None:
            string += "{name}: , ".format(name = prop[0])
        else:
            string += "{name}: {value}, ".format(name = prop[0], value = value)
    return string[:-2]

def toWaveData(jsonObj):
    # Many JSON implementations leave default values out.  We compensate for WaveData, knowing
    # that all values should be filled in
    wave = WaveData()
    properties = inspect.getmembers(type(wave), isprop)
    for prop in properties:
        # Pre-Assign the default
        prop[1].fset(wave, 0)

        # 
        if prop[0] in jsonObj:
            value = jsonObj[prop[0]]
            if value is not None:
                prop[1].fset(wave, value)
    return wave


######################################################################################################
# The following define the identifiers we'll use throughout
######################################################################################################

sampleTypeId = "WaveData_SampleType"
sampleTargetTypeId = "WaveDataTarget_SampleType"
sampleIntegerTypeId = "WaveData_IntegerType"
sampleStreamId = "WaveData_SampleStream"
sampleBehaviorId = "WaveData_SampleBehavior"
sampleStreamViewId = "WaveData_SampleStreamView"
sampleStreamViewIntId = "WaveData_SampleIntStreamView"
sampleDataviewId = "WaveData_Dataview"

try:
    config = configparser.ConfigParser()
    config.read('config.ini')


    print("------------------------------------------")
    print("  _________    .___     __________        ")        
    print(" /   _____/  __| _/_____\______   \___.__.")
    print(" \_____  \  / __ |/  ___/|     ___<   |  |")
    print(" /        \/ /_/ |\___ \ |    |    \___  |")
    print("/_______  /\____ /____  >|____|    / ____|")
    print("        \/      \/    \/           \/     ")	
    print("------------------------------------------")

    client = SdsClient(config.get('Access', 'Tenant'), config.get('Access', 'Address'), config.get('Credentials', 'Resource'),
                      config.get('Credentials', 'Authority'), config.get('Credentials', 'ClientId'), config.get('Credentials', 'ClientSecret'))

    namespaceId = config.get('Configurations', 'Namespace')

    print("Sds endpoint at {url}".format(url = client.Uri))
    print

    ######################################################################################################
    # SdsType get or creation
    ######################################################################################################
    print("Creating an SdsType")
    waveType = getWaveDataType(sampleTypeId)
    waveType = client.getOrCreateType(namespaceId, waveType)

    ######################################################################################################
    # Sds Stream creation
    ######################################################################################################
    print("Creating an SdsStream")
    stream = SdsStream()
    stream.Id = sampleStreamId
    stream.Name = "WaveStreamPySample"
    stream.Description = "A Stream to store the WaveData events"
    stream.TypeId = waveType.Id
    stream.BehaviorId = None
    client.createOrUpdateStream(namespaceId, stream)

    ######################################################################################################
    # CRUD operations for events
    ######################################################################################################

    start = datetime.datetime.now()
    span = datetime.datetime.strptime("0:1:0", "%H:%M:%S")
    print("Inserting data")
    # Insert a single event
    event = nextWave(start, span, 2.0, 0)
    client.insertValue(namespaceId, stream.Id, event)

    # Insert a list of events
    waves = []
    for i in range(2, 20, 2):
        waves.append(nextWave(start + datetime.timedelta(seconds = i * 0.2), span, 2.0, i))
    client.insertValues(namespaceId, stream.Id, waves)

    # Get the last inserted event in a stream
    print("Getting latest event")
    wave = client.getLastValue(namespaceId, stream.Id, WaveData)
    print(toString(wave))
    print

    # Get all the events
    waves = client.getWindowValues(namespaceId, stream.Id, WaveData, 0, 40)
    print("Getting all events")
    print("Total events found: " + str(len(waves)))
    for wave in waves:
        print(toString(wave))
    print
    
    print("Updating events")
    # Update the first event
    event = nextWave(start, span, 4.0, 0)
    client.updateValue(namespaceId, stream.Id, event)

    # Update the rest of the events, adding events that have no prior index entry
    updatedEvents = []
    for i in range(2, 40, 2):
        event = nextWave(start + datetime.timedelta(seconds = i * 0.2), span, 4.0, i)
        updatedEvents.append(event)
    client.updateValues(namespaceId, stream.Id, updatedEvents)

    # Get all the events
    waves = client.getWindowValues(namespaceId, stream.Id, WaveData, 0, 40)
    print("Getting updated events")
    print("Total events found: " + str(len(waves)))
    for wave in waves:
        print(toString(wave))
    print

    print("Replacing events")
    # replace one value
    event = nextWave(start, span, 10.0, 0)
    client.replaceValue(namespaceId, stream.Id, event)
    
    # replace multiple values
    replacedEvents = []
    for i in range(2, 40, 2):
        event = nextWave(start + datetime.timedelta(seconds=i * 0.2), span, 10.0, i)
        replacedEvents.append(event)
    client.replaceValues(namespaceId, stream.Id, replacedEvents)

    # Get all the events
    waves = client.getWindowValues(namespaceId, stream.Id, WaveData, 0, 40)
    print("Getting replaced events")
    print("Total events found: " + str(len(waves)))
    for wave in waves:
        print(toString(wave))
    print
    ######################################################################################################
    # Property Overrides
    ######################################################################################################
    
    print("Property Overrides")
    print("Sds can interpolate or extrapolate data at an index location where data does not explicitly exist:")
    print
    
	# We will retrieve three events using the default behavior, Continuous
    waves = client.getRangeValues(namespaceId, stream.Id, WaveData, "1", 0, 3, False, SdsBoundaryType.ExactOrCalculated)

    print("Default (Continuous) requesting data starting at index location '1', where we have not entered data, Sds will interpolate a value for each property:")
    for wave in waves:
        print(("Order: {order}: Radians: {radians} Cos: {cos}".format(order = wave.Order, radians = wave.Radians, cos = wave.Cos)))

    # Create a Discrete stream PropertyOverride indicating that we do not want Sds to calculate a value for Radians and update our stream 
    propertyOverride = SdsStreamPropertyOverride()
    propertyOverride.SdsTypePropertyId = 'Radians'
    propertyOverride.InterpolationMode = 3

    props = [propertyOverride]
    stream.PropertyOverrides = props
    client.createOrUpdateStream(namespaceId, stream)

    waves = client.getRangeValues(namespaceId, stream.Id, WaveData, "1", 0, 3, False, SdsBoundaryType.ExactOrCalculated)
    print
    print("We can override this behavior on a property by property basis, here we override the Radians property instructing Sds not to interpolate.")
    print("Sds will now return the default value for the data type:")
    for wave in waves:
        print(("Order: {order}: Radians: {radians} Cos: {cos}".format(order = wave.Order, radians = wave.Radians, cos = wave.Cos)))


    ######################################################################################################
    # Stream Views
    ######################################################################################################

    #Create additional types to define our targets
    waveTargetType = getWaveDataTargetType(sampleTargetTypeId)
    waveTargetType = client.getOrCreateType(namespaceId, waveTargetType)

    waveIntegerType = getWaveDataIntegerType(sampleIntegerTypeId)
    waveIntegerType = client.getOrCreateType(namespaceId, waveIntegerType)

    #Create an SdsStreamViewProperty objects when we want to explicitly map one property to another
    vp1 = SdsStreamViewProperty()
    vp1.SourceId = "Order"
    vp1.TargetId = "OrderTarget"

    vp2 = SdsStreamViewProperty()
    vp2.SourceId = "Sin"
    vp2.TargetId = "SinInt"
    
    vp3 = SdsStreamViewProperty()
    vp3.SourceId = "Cos"
    vp3.TargetId = "CosInt"
    
    vp4 = SdsStreamViewProperty()
    vp4.SourceId = "Tan"
    vp4.TargetId = "TanInt"
    
    #Create a streamView mapping our original type to our target type, data shape is the same so let Sds handle the mapping
    streamView = SdsStreamView()
    streamView.Id = sampleStreamViewId
    streamView.Name = "SampleStreamView"
    streamView.TargetTypeId = waveTargetType.Id
    streamView.SourceTypeId = waveType.Id

    #Data shape and data types are different so include explicit mappings between properties
    manualStreamView = SdsStreamView()
    manualStreamView.Id = sampleStreamViewIntId
    manualStreamView.Name = "SampleIntStreamView"
    manualStreamView.TargetTypeId = waveIntegerType.Id
    manualStreamView.SourceTypeId = waveType.Id
    manualStreamView.Properties = [vp1, vp2, vp3, vp4]
    
    automaticStreamView = client.getOrCreateStreamView(namespaceId, streamView)
    manualStreamView = client.getOrCreateStreamView(namespaceId, manualStreamView)
    
    streamViewMap1 = SdsStreamViewMap()
    streamViewMap1 = client.getStreamViewMap(namespaceId, automaticStreamView.Id)

    streamViewMap2 = SdsStreamViewMap()
    streamViewMap2 = client.getStreamViewMap(namespaceId, manualStreamView.Id)

    rangeWaves = client.getRangeValues(namespaceId, stream.Id, WaveData, "1", 0, 3, False, SdsBoundaryType.ExactOrCalculated)
    print
    print("SdsStreamViews")
    print("Here is some of our data as it is stored on the server:")
    for way in rangeWaves:
        print(("Sin: {sin}, Cos: {cos}, Tan: {tan}".format(sin = way.Sin, cos = way.Cos, tan = way.Tan)))

    #StreamView data when retrieved with a streamView
    rangeWaves = client.getRangeValues(namespaceId, stream.Id, WaveDataTarget, "1", 0, 3, False, SdsBoundaryType.ExactOrCalculated, automaticStreamView.Id)
    print
    print("Specifying a streamView with an SdsType of the same shape returns values that are automatically mapped to the target SdsType's properties:")
    for way in rangeWaves:
        print(("SinTarget: {sinTarget}, CosTarget: {cosTarget}, TanTarget: {tanTarget}".format(sinTarget = way.SinTarget, cosTarget = way.CosTarget, tanTarget = way.TanTarget)))

    rangeWaves = client.getRangeValues(namespaceId, stream.Id, WaveDataInteger, "1", 0, 3, False, SdsBoundaryType.ExactOrCalculated, manualStreamView.Id)
    print
    print("SdsStreamViews can also convert certain types of data, here we return integers where the original values were doubles:")
    for way in rangeWaves:
        print(("SinInt: {sinInt}, CosInt: {cosInt}, TanInt: {tanInt}".format(sinInt = way.SinInt, cosInt = way.CosInt, tanInt = way.TanInt)))

    print
    print ("We can query Sds to return the SdsStreamViewMap for our SdsStreamView, here is the one generated automatically:")
    for prop in streamViewMap1.Properties:
        print(("{source} => {dest}".format(source = prop.SourceId, dest = prop.TargetId)))
		
    print
    print ("Here is our explicit mapping, note SdsStreamViewMap will return all properties of the Source Type, even those without a corresponding Target property:")
    for prop in streamViewMap2.Properties:
        if hasattr(prop,'TargetId'):
            print(("{source} => {dest}".format(source = prop.SourceId, dest = prop.TargetId)))
        else:
            print(("{source} => {dest}".format(source = prop.SourceId, dest = 'Not mapped')))
			
	######################################################################################################
    # Tags and Metadata
    ######################################################################################################
    print
    print("Let's add some Tags and Metadata to our stream:")

    tags = ["waves", "periodic", "2018", "validated"]
    metadata = { "Region":"North America" , "Country":"Canada","Province":"Quebec" }

    client.createOrUpdateTags(namespaceId, stream.Id, tags)
    client.createOrUpdateMetadata(namespaceId, stream.Id, metadata)

    print
    print("Tags now associated with " + stream.Id)
    tags = client.getTags(namespaceId, stream.Id)
    for x in range(len(tags)):
        print(tags[x])

    region = client.getMetadata(namespaceId, stream.Id, "Region")
    country = client.getMetadata(namespaceId, stream.Id, "Country")
    province = client.getMetadata(namespaceId, stream.Id, "Province")

    print
    print("Metadata now associated with" + stream.Id + ":")
    print("Metadata key Region: " + region)
    print("Metadata key Country: " + country)
    print("Metadata key Province: " + province)
    print

    ######################################################################################################
    # Delete events
    ######################################################################################################
    print
    print('Deleting values from the SdsStream')
    # remove a single value from the stream
    client.removeValue(namespaceId, stream.Id, 0)

    # remove multiple values from the stream
    client.removeWindowValues(namespaceId, stream.Id, 0, 40)
    try:
        event = client.getLastValue(namespaceId, stream.Id, WaveData)
        if event != None:
            raise ValueError
    except TypeError:
        pass
    print("All values deleted successfully!")

except Exception as ex:
    print(("Encountered Error: {error}".format(error = ex)))
    print

finally:
    ######################################################################################################
    # SdsType, SdsStream, SdsStreamView and SdsBehavior deletion
    ######################################################################################################

    # Clean up the remaining artifacts
    print("Cleaning up")

    print("Deleting the stream")
    supressError(lambda: client.deleteStream(namespaceId, sampleStreamId))

    print("Deleting the streamViews")
    supressError(lambda: client.deleteStreamView(namespaceId, sampleStreamViewId))
    supressError(lambda: client.deleteStreamView(namespaceId, sampleStreamViewIntId))

    print("Deleting the types")
    supressError(lambda: client.deleteType(namespaceId, sampleTypeId))
    supressError(lambda: client.deleteType(namespaceId, sampleTargetTypeId))
    supressError(lambda: client.deleteType(namespaceId, sampleIntegerTypeId))
	
    print("Deleting dataview")
    supressError(lambda: client.deleteDataview(namespaceId, sampleDataviewId))

print("done")
