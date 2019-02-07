from ocs_sample_library_preview import OCSClient, DataviewClient, SdsClient
import configparser
  



config = configparser.ConfigParser()
config.read('config.ini')

#print(o.OCSClient)
client: OCSClient = OCSClient(config.get('Access', 'ApiVersion'),config.get('Access', 'Tenant'), config.get('Access', 'Resource'), 
                     config.get('Credentials', 'ClientId'), config.get('Credentials', 'ClientSecret'))

namespaceId = config.get('Configurations', 'Namespace')

dvc:DataviewClient =client.Dataview
svc: SdsClient = client.Sds 


streams = svc.getStreams(namespaceId)
for stream in streams:
    print(stream.toJson())

#print(client.DataviewClient)
#namespaceId = config.get('Configurations', 'Namespace')
#s = client.DataviewClient
#s.G
#print(s)