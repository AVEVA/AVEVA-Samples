from ocs_sample_library_preview import OCSClient, Streams
import configparser
  

config = configparser.ConfigParser()
config.read('config.ini')

client: OCSClient = OCSClient(config.get('Access', 'ApiVersion'),config.get('Access', 'Tenant'), config.get('Access', 'Resource'), 
                     config.get('Credentials', 'ClientId'), config.get('Credentials', 'ClientSecret'))

namespaceId = config.get('Configurations', 'Namespace')

#This doesn't seem necessary, but it allows VS Code to figure out the intellisense and what is going on.  Not needed during an import, just in the local test.
#Maybe there is a local setting to try here
sss: Streams = client.Streams


streams = client.Streams.getStreams(namespaceId)

for stream in streams:
    print(stream.toJson())
