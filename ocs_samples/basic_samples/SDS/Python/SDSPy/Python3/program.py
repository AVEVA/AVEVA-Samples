# program.py
#
# version 0.0.2

import configparser
import inspect
import math

from ocs_sample_library_preview import (SdsType, SdsTypeCode, SdsTypeProperty,
                                        OCSClient, SdsStream, SdsBoundaryType,
                                        SdsStreamPropertyOverride,
                                        SdsStreamViewProperty, SdsStreamView,
                                        SdsStreamViewMap, SdsStreamIndex)

from WaveData import (WaveData, WaveDataCompound, WaveDataInteger,
                      WaveDataTarget)


# returns a type that represents the WaveData data
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

    # create an SdsType for WaveData Class
    wave = SdsType()
    wave.Id = sampleTypeId
    wave.Name = "WaveDataSample"
    wave.Description = "This is a sample Sds type for storing WaveData type "\
                       "events."
    wave.SdsTypeCode = SdsTypeCode.Object
    wave.Properties = [orderProperty, tauProperty, radiansProperty,
                       sinProperty, cosProperty, tanProperty,
                       sinhProperty, coshProperty, tanhProperty]

    return wave


# returns a type that represents the WaveData data
def getWaveCompoundDataType(sampleTypeId):
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
    orderProperty.Order = 1

    multiplierProperty = SdsTypeProperty()
    multiplierProperty.Id = "Multiplier"
    multiplierProperty.SdsType = intType
    multiplierProperty.IsKey = True
    multiplierProperty.Order = 2

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

    # create an SdsType for WaveData Class
    wave = SdsType()
    wave.Id = sampleTypeId
    wave.Name = "WaveDataTypeCompound"
    wave.Description = "This is a sample Sds type for storing WaveData type "\
                       "events"
    wave.SdsTypeCode = SdsTypeCode.Object
    wave.Properties = [orderProperty, multiplierProperty, tauProperty,
                       radiansProperty, sinProperty, cosProperty, tanProperty,
                       sinhProperty, coshProperty, tanhProperty]

    return wave


# returns a type that represents the WaveDataTarget data
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

    # create an SdsType for WaveData Class
    wave = SdsType()
    wave.Id = sampleTargetTypeId
    wave.Name = "WaveDataTargetSample"
    wave.Description = "This is a sample Sds type for storing WaveDataTarget"\
                       " type events"
    wave.SdsTypeCode = SdsTypeCode.Object
    wave.Properties = [orderTargetProperty, tauTargetProperty,
                       radiansTargetProperty, sinTargetProperty,
                       cosTargetProperty, tanTargetProperty,
                       sinhTargetProperty, coshTargetProperty,
                       tanhTargetProperty]

    return wave


# returns a type that represents WaveDataInteger data
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

    # create an SdsType for the WaveDataInteger Class
    wave = SdsType()
    wave.Id = sampleIntegerTypeId
    wave.Name = "WaveDataIntegerSample"
    wave.Description = "This is a sample Sds type for storing WaveDataInteger"\
                       "type events"
    wave.SdsTypeCode = SdsTypeCode.Object
    wave.Properties = [orderTargetProperty, sinIntProperty,
                       cosIntProperty, tanIntProperty]

    return wave


# Generate a new WaveData event
def nextWave(order, multiplier):
    radians = (order) * math.pi/32

    newWave = WaveDataCompound()
    newWave.Order = order
    newWave.Multiplier = multiplier
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
        print(f"Encountered Error: {e}")


def isprop(v):
    return isinstance(v, property)


def toString(event):
    string = ""
    props = inspect.getmembers(type(event), isprop)
    printOrder = [2, 3, 4, 0, 6, 5, 1, 7, 8]
    orderedProps = [props[i] for i in printOrder]
    for prop in orderedProps:
        value = prop[1].fget(event)
        if value is None:
            string += "{name}: , ".format(name=prop[0])
        else:
            string += "{name}: {value}, ".format(name=prop[0], value=value)
    return string[:-2]


def toWaveData(jsonObj):
    # Many JSON implementations leave default values out.  We compensate for
    # WaveData, knowing  that all values should be filled in
    wave = WaveData()
    properties = inspect.getmembers(type(wave), isprop)
    for prop in properties:
        # Pre-Assign the default
        prop[1].fset(wave, 0)

        if prop[0] in jsonObj:
            value = jsonObj[prop[0]]
            if value is not None:
                prop[1].fset(wave, value)
    return wave


###############################################################################
# The following define the identifiers we'll use throughout
###############################################################################

sampleTypeId = "WaveData_SampleType"
sampleTargetTypeId = "WaveDataTarget_SampleType"
sampleIntegerTypeId = "WaveData_IntegerType"
sampleStreamId = "WaveData_SampleStream"
sampleStreamViewId = "WaveData_SampleStreamView"
sampleStreamViewIntId = "WaveData_SampleIntStreamView"
streamIdSecondary = "SampleStream_Secondary"
streamIdCompound = "SampleStream_Compound"
compoundTypeId = "SampleType_Compound"


def main():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')

        # Step 1
        ocsClient = OCSClient(config.get('Access', 'ApiVersion'),
                              config.get('Access', 'Tenant'),
                              config.get('Access', 'Resource'),
                              config.get('Credentials', 'ClientId'),
                              config.get('Credentials', 'ClientSecret'))

        namespaceId = config.get('Configurations', 'Namespace')

        print(r"------------------------------------------")
        print(r"  _________    .___     __________        ")
        print(r" /   _____/  __| _/_____\______   \___.__.")
        print(r" \_____  \  / __ |/  ___/|     ___<   |  |")
        print(r" /        \/ /_/ |\___ \ |    |    \___  |")
        print(r"/_______  /\____ /____  >|____|    / ____|")
        print(r"        \/      \/    \/           \/     ")
        print(r"------------------------------------------")
        print("Sds endpoint at {url}".format(url=ocsClient.uri))
        print()

        # Step 2
        #######################################################################
        # SdsType get or creation
        #######################################################################
        print("Creating an SdsType")
        waveType = getWaveDataType(sampleTypeId)
        waveType = ocsClient.Types.getOrCreateType(namespaceId, waveType)
        assert waveType.Id == sampleTypeId, "Error getting back wave Type"

        # Step 3
        #######################################################################
        # Sds Stream creation
        #######################################################################
        print("Creating an SdsStream")
        stream = SdsStream()
        stream.Id = sampleStreamId
        stream.Name = "WaveStreamPySample"
        stream.Description = "A Stream to store the WaveData events"
        stream.TypeId = waveType.Id
        ocsClient.Streams.createOrUpdateStream(namespaceId, stream)

        # Step 4
        #######################################################################
        # CRUD operations for events
        #######################################################################

        print("Inserting data")
        # Insert a single event
        event = nextWave(0, 2.0)
        ocsClient.Streams.insertValues(namespaceId, stream.Id, [event])

        # Insert a list of events
        waves = []
        for i in range(2, 20, 2):
            waves.append(nextWave(i, 2.0))
        ocsClient.Streams.insertValues(namespaceId, stream.Id, waves)

        # Step 5
        # Get the last inserted event in a stream
        print("Getting latest event")
        wave = ocsClient.Streams.getLastValue(namespaceId, stream.Id, WaveData)
        print(toString(wave))
        print()

        # Get all the events
        waves = ocsClient.Streams.getWindowValues(
            namespaceId, stream.Id, WaveData, 0, 180)
        print("Getting all events")
        print("Total events found: " + str(len(waves)))
        for wave in waves:
            print(toString(wave))
        print()

        # Step 6
        # get all values with headers
        waves = ocsClient.Streams.getWindowValuesForm(
            namespaceId, stream.Id, None, 0, 180, "tableh")
        print("Getting all events in table format")
        print(waves)

        # Step 7
        print("Updating events")
        # Update the first event
        event = nextWave(0, 4.0)
        ocsClient.Streams.updateValues(namespaceId, stream.Id, [event])

        # Update the rest of the events, adding events that have no prior
        # index entry
        updatedEvents = []
        for i in range(2, 40, 2):
            event = nextWave(i, 4.0)
            updatedEvents.append(event)
        ocsClient.Streams.updateValues(namespaceId, stream.Id, updatedEvents)

        # Get all the events
        waves = ocsClient.Streams.getWindowValues(namespaceId, stream.Id,
                                                  WaveData, 0, 40)
        print("Getting updated events")
        print("Total events found: " + str(len(waves)))
        for wave in waves:
            print(toString(wave))
        print()

        # Step 8
        print("Replacing events")
        # replace one value
        event = nextWave(0, 5.0)
        ocsClient.Streams.replaceValues(namespaceId, stream.Id, [event])

        # replace multiple values
        replacedEvents = []
        for i in range(2, 40, 2):
            event = nextWave(i, 5.0)
            replacedEvents.append(event)
        ocsClient.Streams.replaceValues(namespaceId, stream.Id, replacedEvents)

        # Step 9
        # Get all the events
        waves = ocsClient.Streams.getWindowValues(namespaceId, stream.Id,
                                                  WaveData, 0, 180)
        print("Getting replaced events")
        print("Total events found: " + str(len(waves)))
        for wave in waves:
            print(toString(wave))
        print()

        retrievedInterpolated = ocsClient.Streams.getRangeValuesInterpolated(
            namespaceId, stream.Id, None, "5", "32", 4)
        print("Sds can interpolate or extrapolate data at an index location "
              "where data does not explicitly exist:")
        print(retrievedInterpolated)
        print()

        # Step 10
        # Filtering from all values
        print("Getting filtered events")
        filteredEvents = ocsClient.Streams.getWindowValues(
            namespaceId, sampleStreamId, WaveData, 0, 50, 'Radians lt 3')

        print("Total events found: " + str(len(filteredEvents)))
        for wave in filteredEvents:
            print(toString(wave))
        print()

        # Step 11
        # Sampling from all values
        print("Getting sampled values")
        sampledWaves = ocsClient.Streams.getSampledValues(
            namespaceId, stream.Id, WaveData, 0, 40, "sin", 4)

        print("Total events found: " + str(len(sampledWaves)))
        for wave in sampledWaves:
            print(toString(wave))
        print()

        # Step 12
        #######################################################################
        # Property Overrides
        #######################################################################

        print("Property Overrides")
        print("Sds can interpolate or extrapolate data at an index location "
              "where data does not explicitly exist:")
        print()

        # We will retrieve three events using the default behavior, Continuous
        waves = ocsClient.Streams.getRangeValues(
            namespaceId, stream.Id, WaveData, "1", 0, 3, False,
            SdsBoundaryType.ExactOrCalculated)

        print("Default (Continuous) requesting data starting at index location"
              " '1', where we have not entered data, Sds will interpolate a "
              "value for each property:")

        for wave in waves:
            print(("Order: {order}: Radians: {radians} Cos: {cos}".format(
                order=wave.Order, radians=wave.Radians, cos=wave.Cos)))

        # Create a Discrete stream PropertyOverride indicating that we do not
        #  want Sds to calculate a value for Radians and update our stream
        propertyOverride = SdsStreamPropertyOverride()
        propertyOverride.SdsTypePropertyId = 'Radians'
        propertyOverride.InterpolationMode = 3

        # update the stream
        props = [propertyOverride]
        stream.PropertyOverrides = props
        ocsClient.Streams.createOrUpdateStream(namespaceId, stream)

        waves = ocsClient.Streams.getRangeValues(
            namespaceId, stream.Id, WaveData, "1", 0, 3, False,
            SdsBoundaryType.ExactOrCalculated)
        print()
        print("We can override this read behavior on a property by property"
              "basis, here we override the Radians property instructing Sds"
              " not to interpolate.")
        print("Sds will now return the default value for the data type:")
        for wave in waves:
            print(("Order: {order}: Radians: {radians} Cos: {cos}".format(
                order=wave.Order, radians=wave.Radians, cos=wave.Cos)))

        # Step 13
        #######################################################################
        # Stream Views
        #######################################################################

        # Create additional types to define our targets
        waveTargetType = getWaveDataTargetType(sampleTargetTypeId)
        waveTargetType = ocsClient.Types.getOrCreateType(namespaceId,
                                                         waveTargetType)

        waveIntegerType = getWaveDataIntegerType(sampleIntegerTypeId)
        waveIntegerType = ocsClient.Types.getOrCreateType(namespaceId,
                                                          waveIntegerType)

        # Create an SdsStreamViewProperty objects when we want to explicitly
        # map one property to another
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

        # Create a streamView mapping our original type to our target type,
        # data shape is the same so let Sds handle the mapping
        streamView = SdsStreamView()
        streamView.Id = sampleStreamViewId
        streamView.Name = "SampleStreamView"
        streamView.TargetTypeId = waveTargetType.Id
        streamView.SourceTypeId = waveType.Id

        # Data shape and data types are different so include explicit mappings
        # between properties
        manualStreamView = SdsStreamView()
        manualStreamView.Id = sampleStreamViewIntId
        manualStreamView.Name = "SampleIntStreamView"
        manualStreamView.TargetTypeId = waveIntegerType.Id
        manualStreamView.SourceTypeId = waveType.Id
        manualStreamView.Properties = [vp1, vp2, vp3, vp4]

        automaticStreamView = ocsClient.Streams.getOrCreateStreamView(
            namespaceId, streamView)
        manualStreamView = ocsClient.Streams.getOrCreateStreamView(
            namespaceId, manualStreamView)

        streamViewMap1 = SdsStreamViewMap()
        streamViewMap1 = ocsClient.Streams.getStreamViewMap(
            namespaceId, automaticStreamView.Id)

        streamViewMap2 = SdsStreamViewMap()
        streamViewMap2 = ocsClient.Streams.getStreamViewMap(
            namespaceId, manualStreamView.Id)

        rangeWaves = ocsClient.Streams.getRangeValues(
            namespaceId, stream.Id, WaveData, "1", 0, 3, False,
            SdsBoundaryType.ExactOrCalculated)
        print()
        print("SdsStreamViews")
        print("Here is some of our data as it is stored on the server:")
        for way in rangeWaves:
            print(("Sin: {sin}, Cos: {cos}, Tan: {tan}".format(
                sin=way.Sin, cos=way.Cos, tan=way.Tan)))

        # StreamView data when retrieved with a streamView
        rangeWaves = ocsClient.Streams.getRangeValues(
            namespaceId, stream.Id, WaveDataTarget, "1", 0, 3, False,
            SdsBoundaryType.ExactOrCalculated, automaticStreamView.Id)
        print()
        print("Specifying a streamView with an SdsType of the same shape"
              "returns values that are automatically mapped to the target"
              " SdsType's properties:")
        for way in rangeWaves:
            print(("SinTarget: {sinTarget}, CosTarget: {cosTarget}, TanTarget:"
                   " {tanTarget}").format(sinTarget=way.SinTarget,
                                          cosTarget=way.CosTarget,
                                          tanTarget=way.TanTarget))

        rangeWaves = ocsClient.Streams.getRangeValues(
            namespaceId, stream.Id, WaveDataInteger, "1", 0, 3, False,
            SdsBoundaryType.ExactOrCalculated, manualStreamView.Id)
        print()
        print("SdsStreamViews can also convert certain types of data, here we"
              " return integers where the original values were doubles:")
        for way in rangeWaves:
            print(("SinInt: {sinInt}, CosInt: {cosInt}, TanInt: {tanInt}")
                  .format(sinInt=way.SinInt, cosInt=way.CosInt,
                          tanInt=way.TanInt))

        print()
        print("We can query Sds to return the SdsStreamViewMap for our "
              "SdsStreamView, here is the one generated automatically:")
        for prop in streamViewMap1.Properties:
            print(("{source} => {dest}".format(
                source=prop.SourceId, dest=prop.TargetId)))

        print()
        print("Here is our explicit mapping, note SdsStreamViewMap will return"
              " all properties of the Source Type, even those without a "
              "corresponding Target property:")
        for prop in streamViewMap2.Properties:
            if hasattr(prop, 'TargetId'):
                print(("{source} => {dest}".format(source=prop.SourceId,
                                                   dest=prop.TargetId)))
            else:
                print(("{source} => {dest}".format(source=prop.SourceId,
                                                   dest='Not mapped')))

        # Step 14
        print("We will now update the stream type based on the streamview")

        firstVal = ocsClient.Streams.getFirstValue(namespaceId, stream.Id,
                                                   None)
        ocsClient.Streams.updateStreamType(namespaceId, stream.Id,
                                           sampleStreamViewId)

        newStream = ocsClient.Streams.getStream(namespaceId, sampleStreamId)
        firstValUpdated = ocsClient.Streams.getFirstValue(namespaceId,
                                                          sampleStreamId, None)

        print("The new type id" + newStream.TypeId + " compared to the "
              "original one " + stream.TypeId)
        print("The new type value " + str(firstVal) + " compared to the "
              "original one " + str(firstValUpdated))

        # Step 15
        types = ocsClient.Types.getTypes(namespaceId, 0, 100)
        typesQuery = ocsClient.Types.getTypes(
            namespaceId, 0, 100, "Id:*Target*")

        print()
        print("All Types: ")
        for typeI in types:
            print(typeI.Id)

        print("Types after Query: ")
        for typeI in typesQuery:
            print(typeI.Id)

        # Step 16
        #######################################################################
        # Tags and Metadata
        #######################################################################
        print()
        print("Let's add some Tags and Metadata to our stream:")

        tags = ["waves", "periodic", "2018", "validated"]
        metadata = {"Region": "North America", "Country": "Canada",
                    "Province": "Quebec"}

        ocsClient.Streams.createOrUpdateTags(namespaceId, stream.Id, tags)
        ocsClient.Streams.createOrUpdateMetadata(namespaceId, stream.Id,
                                                 metadata)

        print()
        print("Tags now associated with ", stream.Id)
        print(ocsClient.Streams.getTags(namespaceId, stream.Id))

        region = ocsClient.Streams.getMetadata(
            namespaceId, stream.Id, "Region")
        country = ocsClient.Streams.getMetadata(
            namespaceId, stream.Id, "Country")
        province = ocsClient.Streams.getMetadata(
            namespaceId, stream.Id, "Province")

        print()
        print("Metadata now associated with", stream.Id, ":")
        print("Metadata key Region: ", region)
        print("Metadata key Country: ", country)
        print("Metadata key Province: ", province)
        print()

        # Step 17
        #######################################################################
        # Delete events
        #######################################################################
        print()
        print('Deleting values from the SdsStream')
        # remove a single value from the stream
        ocsClient.Streams.removeValue(namespaceId, stream.Id, 0)

        # remove multiple values from the stream
        ocsClient.Streams.removeWindowValues(namespaceId, stream.Id, 0, 40)
        try:
            event = ocsClient.Streams.getLastValue(namespaceId, stream.Id,
                                                   WaveData)
            if event is not None:
                raise ValueError
        except TypeError:
            pass
        print("All values deleted successfully!")

        # Step 18
        print("Adding a stream with a secondary index.")
        index = SdsStreamIndex()
        index.SdsTypePropertyId = "Radians"

        secondary = SdsStream()
        secondary.Id = streamIdSecondary
        secondary.TypeId = sampleTypeId
        secondary.Indexes = [index]

        secondary = ocsClient.Streams.getOrCreateStream(namespaceId, secondary)
        count = 0
        if(stream.Indexes):
            count = len(stream.Indexes)

        print("Secondary indexes on streams original:" + str(count) +
              ". New one:  " + str(len(secondary.Indexes)))
        print()

        # Modifying an existing stream with a secondary index.
        print("Modifying a stream to have a secondary index.")

        sampleStream = ocsClient.Streams.getStream(namespaceId, sampleStreamId)

        index = SdsStreamIndex()
        index.SdsTypePropertyId = "RadiansTarget"
        sampleStream.Indexws = [index]
        ocsClient.Streams.createOrUpdateStream(namespaceId, sampleStream)

        sampleStream = ocsClient.Streams.getStream(namespaceId, sampleStreamId)
        # Modifying an existing stream to remove the secondary index
        print("Removing a secondary index from a stream.")

        secondary.Indexes = []

        ocsClient.Streams.createOrUpdateStream(namespaceId, secondary)

        secondary = ocsClient.Streams.getStream(namespaceId, secondary.Id)

        originalLength = "0"
        if stream.Indexes:
            originalLength = str(len(stream.Indexes))

        secondaryLength = "0"
        if secondary.Indexes:
            secondaryLength = str(len(secondary.Indexes))

        print("Secondary indexes on streams original:" + originalLength +
              ". New one:  " + secondaryLength)

        # Step 19
        # Adding Compound Index Type
        print("Creating an SdsType with a compound index")
        typeCompound = getWaveCompoundDataType(compoundTypeId)
        ocsClient.Types.getOrCreateType(namespaceId, typeCompound)

        # create an SdsStream
        print("Creating an SdsStream off of type with compound index")
        streamCompound = SdsStream()
        streamCompound.Id = streamIdCompound
        streamCompound.TypeId = typeCompound.Id
        ocsClient.Streams.createOrUpdateStream(namespaceId, streamCompound)

        # Step 20
        print("Inserting data")
        waves = []
        waves.append(nextWave(1, 10))
        waves.append(nextWave(2, 2))
        waves.append(nextWave(3, 1))
        waves.append(nextWave(10, 3))
        waves.append(nextWave(10, 8))
        waves.append(nextWave(10, 10))
        ocsClient.Streams.insertValues(namespaceId, streamIdCompound, waves)

        latestCompound = ocsClient.Streams.getLastValue(
            namespaceId, streamIdCompound, None)
        firstCompound = ocsClient.Streams.getFirstValue(
            namespaceId, streamIdCompound, None)

        windowVal = ocsClient.Streams.getWindowValues(
            namespaceId, streamIdCompound, None, "2|1", "10|8")

        print("First data: " + str(firstCompound) +
              " Latest data: " + str(latestCompound))
        print("Window Data:")
        print(str(windowVal))

    except Exception as i:
        print(("Encountered Error: {error}".format(error=i)))
        assert False, ("Encountered Error: {error}".format(error=i))
        print()

    finally:
        # Step 21

        #######################################################################
        # SdsType, SdsStream, and SdsStreamView deletion
        #######################################################################
        # Clean up the remaining artifacts
        print("Cleaning up")
        print("Deleting the stream")
        supressError(lambda: ocsClient.Streams.deleteStream(
            namespaceId, sampleStreamId))
        supressError(lambda: ocsClient.Streams.deleteStream(
            namespaceId, streamIdSecondary))
        supressError(lambda: ocsClient.Streams.deleteStream(
            namespaceId, streamIdCompound))

        print("Deleting the streamViews")
        supressError(lambda: ocsClient.Streams.deleteStreamView(
            namespaceId, sampleStreamViewId))
        supressError(lambda: ocsClient.Streams.deleteStreamView(
            namespaceId, sampleStreamViewIntId))

        print("Deleting the types")
        supressError(lambda: ocsClient.Types.deleteType(
            namespaceId, sampleTypeId))
        supressError(lambda: ocsClient.Types.deleteType(
            namespaceId, sampleTargetTypeId))
        supressError(lambda: ocsClient.Types.deleteType(
            namespaceId, sampleIntegerTypeId))
        supressError(lambda: ocsClient.Types.deleteType(
            namespaceId, compoundTypeId))


main()
print("done")


def test_main():
    main()
