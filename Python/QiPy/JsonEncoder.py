from json import JSONEncoder

class Encoder(JSONEncoder):
    def default(self,obj):
        if isinstance(obj, list):
            objJson = []
            for o in obj:
                oJson = {}
                objAttribs = o.__dict__
                for attrib in objAttribs:
                    if objAttribs[attrib] is not None:
                        oJson[attrib] = objAttribs[attrib]
                objJson.append(oJson)
            return objJson
        else:
            objAttribs = obj.__dict__
            objJson = {}
            for attrib in objAttribs:
                if objAttribs[attrib] is not None:
                    objJson[attrib] = objAttribs[attrib]
            return objJson