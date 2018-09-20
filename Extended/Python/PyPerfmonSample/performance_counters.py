import psutil


class PerformanceCounters:
    def __init__(self):
        self.type_dict = {
            "processor": psutil.cpu_times(),
            "memory": psutil.virtual_memory()
        }

    def get_counters(self, type_id):
        return self.type_dict[type_id.lower()]

    def get_counter_names(self, type_id):
        return self.type_dict.get(type_id.lower())._fields
