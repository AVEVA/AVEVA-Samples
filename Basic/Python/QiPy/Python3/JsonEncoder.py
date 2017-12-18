from json import JSONEncoder
import inspect
import collections

def isprop(v):
  return isinstance(v, property)

class Encoder(JSONEncoder):
    def default(self,obj):
        if isinstance(obj, collections.Iterable):
            # Contend with objects that can be iterated over
            objJson = []
            for o in obj:
                objJson.append(default(o))
            return objJson
        else:
            objJson = {}
            properties = inspect.getmembers(type(obj), isprop)
            if len(properties) > 0:
                for property in properties:
                    value = property[1].fget(obj)
                    if value is not None:
                        objJson[property[0]] = value
            else:
                # If we fail to find properties, we simply serialize the attributes
                objAttribs = obj.__dict__
                for attrib in objAttribs:
                    if objAttribs[attrib] is not None:
                        objJson[attrib] = objAttribs[attrib]
            return objJson