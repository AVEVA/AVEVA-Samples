from sdspy import *
from helper_functions import (to_string, cleanup)


def main():
    config = configparser.ConfigParser()
    config.read('./config.ini')

    ###########################################################
    # The following define the identifiers we'll use throughout
    ###########################################################
    client = SdsClient(config.get('Access', 'TenantId'), config.get('Access', 'Address'),
                       config.get('Credentials', 'Resource'), config.get('Credentials', 'Authority'),
                       config.get('Credentials', 'Clientid'), config.get('Credentials', 'ClientSecret'))
    namespace_id = config.get('Configurations', 'Namespace')
    type_names = json.loads(config.get('Configurations', 'TypeNames'))
    prog = Program(client, namespace_id, type_names)
    prog.run()


class Program:
    def __init__(self, client, namespace_id, type_names):
        self.client = client
        self.namespace_id = namespace_id
        self.type_names = type_names
        self.helper_functions = None

    def run(self):
        print("------------------------------------------")
        print("  _________    .___     __________        ")
        print(" /   _____/  __| _/_____\______   \___.__.")
        print(" \_____  \  / __ |/  ___/|     ___<   |  |")
        print(" /        \/ /_/ |\___ \ |    |    \___  |")
        print("/_______  /\____ /____  >|____|    / ____|")
        print("        \/      \/    \/           \/     ")
        print("------------------------------------------")
        print("Sds endpoint at {}".format(self.client.Uri))
        print()

        self.client.type_names = self.type_names
        for type_name in self.type_names:
            #####################################################################
            # SdsType get or creation
            #####################################################################
            print("--------------------------------------")
            print("Creating an Sds Type for '{}'".format(type_name))
            event_type = self.get_category_data_type(type_name)
            event_type = self.client.get_or_create_type(self.namespace_id, event_type)

            #####################################################################
            # Sds Stream creation
            #####################################################################
            print("Creating an Sds Stream for '{}'".format(type_name))
            print("--------------------------------------")
            print()
            stream = SdsStream(stream_id="{}".format(type_name), name="{}".format(type_name),
                               description="A Stream to store '{}' events".format(type_name),
                               type_id=event_type.Id)
            self.client.create_or_update_stream(self.namespace_id, stream)

        start = datetime.datetime.now()
        dur = 30
        freq = 5
        str_types = ""
        for i, name in enumerate(self.type_names):
            if i == len(self.type_names)-1:
                str_types += " and "
            str_types += "'{}'".format(name)
            if i < len(self.type_names)-2:
                str_types += ", "

        print("Streaming events for {} every {} seconds over {} seconds".format(str_types, freq, dur))
        print("-----------------------------------------------------------" +
              ("-" * sum([(len(x)+2) for x in self.type_names])))
        self.gather_data_over_time(
            self.client,
            self.namespace_id,
            duration=dur, frequency=freq)

        for type_name in self.type_names:
            self.get_all_events(type_name, "{}".format(type_name), start)

        # SdsType, SdsStream deletion
        cleanup(self.client, self.namespace_id, self.type_names)

    @staticmethod
    def next_event(type_id, time_key=None):
        event = SdsTypeData(type_id, time_key)
        counters = PC().get_counters(type_id)
        [event.__setattr__(counters._fields[i], value) for i, value in enumerate(counters)]
        return event

    def get_all_events(self, type_id, stream_id, start):
        events = self.client.get_window_values(self.namespace_id,
                                               stream_id,
                                               SdsTypeData(type_id),
                                               str(start),
                                               end=str(datetime.datetime.utcnow()))

        print("Getting all '{}' events".format(type_id))
        print("---------------------" + ("-" * len(type_id)))
        print("Total '{}' events found: {}".format(type_id, str(len(events))))

        for i, event in enumerate(events):
            print("{}. {}".format(i + 1, to_string(event)))
        print()
        return events

    def gather_data_over_time(self, client, namespace_id, duration, frequency):
        i = duration
        while i > 0:
            print("Time remaining: {} seconds".format(i))
            for type_name in self.type_names:
                event = self.next_event(type_name)
                client.insert_value(namespace_id, "{}".format(type_name), event)
                print("Writing '{}' data to {}".format(type_name, "{}".format(type_name)))
            print()
            time.sleep(frequency)
            i -= frequency

    @staticmethod
    def get_category_data_type(type_id):
        if type_id is None or not isinstance(type_id, str):
            raise TypeError('type_id is not an instantiated string')

        event_type = SdsType()
        event_type.Id = type_id
        event_type.Name = type_id
        event_type.Description = "This is a sample Sds type for storing {}Data events".format(type_id)
        event_type.SdsTypeCode = SdsTypeCode.Object
        event_type.Properties = []

        int_type = SdsType()
        int_type.Id = 'intType'
        int_type.SdsTypeCode = SdsTypeCode.Int64

        date_time_type = SdsType()
        date_time_type.Id = 'dateTimeType'
        date_time_type.SdsTypeCode = SdsTypeCode.DateTime

        # time_prop is the primary key
        time_prop = SdsTypeProperty()
        time_prop.Id = 'Time'
        time_prop.SdsType = date_time_type
        time_prop.IsKey = True
        event_type.Properties.append(time_prop)

        # get and append counters to properties
        counters = PC().get_counters(type_id)

        for field in counters._fields:
            prop = SdsTypeProperty()
            prop.Id = field
            prop.Name = field
            prop.SdsType = int_type
            event_type.Properties.append(prop)

        return event_type


if __name__ == "__main__":
    main()
