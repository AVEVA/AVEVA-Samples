def cleanup_single(client, namespace_id, type_id):
    print("Deleting stream, '{}'".format(type_id))
    supress_error(lambda: client.delete_stream(namespace_id, type_id))
    print("Deleting type, '{}'".format(type_id))
    supress_error(lambda: client.delete_type(namespace_id, type_id))


def cleanup(client, namespace_id, types_names):
    print("Cleaning up...")
    for i, type_id in enumerate(types_names):
        cleanup_single(client, namespace_id, type_id)


def to_string(event):
    string = ""
    for k, v in event.__dict__.items():
        if k != 'type_id':
            if k == 'time':
                string = "{}: {}".format(v, string)
            elif v is None:
                string += "{}: , ".format(k)
            else:
                string += "{}: {}, ".format(k, v)
    return string[:-2]


def supress_error(sds_call):
    try:
        sds_call()
    except Exception as e:
        print(("Encountered Error: {error}".format(error=e)))
