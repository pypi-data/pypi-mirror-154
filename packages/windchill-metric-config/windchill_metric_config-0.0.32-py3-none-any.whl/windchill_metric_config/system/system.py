from json import dumps

from windchill_metric_config.description import Description
from windchill_metric_config.system.network import Network


class SystemMetrics:
    def __init__(self):
        self.memory_total_bytes = Description(
            metric_id='process_real_memory_total_bytes',
            desc='system total memory in bytes'
        )
        self.memory_used_bytes = Description(
            metric_id='process_real_memory_used_bytes',
            desc='system used memory in bytes'
        )
        self.cpu_usage = Description(
            metric_id='process_cpu_usage_percent',
            desc='cpu utilisation in percent'
        )
        self.disc_total = Description(
            metric_id='process_disc_total_bytes',
            desc='total disc space in bytes',
            labels=['mount_point']
        )
        self.disc_used = Description(
            metric_id='process_disc_used_bytes',
            desc='used disc space in bytes',
            labels=['mount_point']
        )
        self.users_count = Description(
            metric_id='process_users_total_count',
            desc='count of logged in users on os',
        )
        self.system_boot = Description(
            metric_id='system_boot_timestamp',
            desc='boot timestamp as label in iso format (ex, 2019-09-07T15:50-04:00)',
            labels=['boot_timestamp']
        )
        self.system_stats = Description(
            metric_id='system_stats_info',
            desc='various information about the host system, '
                 '(logical cpu count, machine, node, physical_cpu_count, processor, os system, version and release)',
            labels=['system', 'version', 'processor', 'node',
                    'physical_cpu_count', 'release', 'logical_cpu_count',
                    'machine', 'fqdn']
        )
        self.network = Network()

        self.services = Description(
            metric_id='process_windows_service_status',
            desc='windows service information (only available on windows machines)',
            labels=['name', 'username', 'start_type', 'status', 'display_name']
        )

    def __str__(self):
        return dumps(self.as_dict())

    def as_dict(self):
        all_metrics = {}
        for item in self.__dict__.keys():
            all_metrics[item] = self.__getattribute__(item).as_dict()
        return all_metrics

    def as_yaml_dict(self):
        metrics = {}
        for item in self.__dict__.keys():
            child = self.__getattribute__(item)
            if type(child) == Description:
                metrics[child.id] = child.enabled
            else:
                metrics[item] = child.as_yaml_dict()
        return metrics

    def as_treeview(self):
        metrics = []
        for item in self.__dict__.keys():
            child = self.__getattribute__(item)
            tree_item = {}
            if type(child) == Description:
                tree_item['text'] = child.id
                tree_item['state'] = {'checked': child.enabled}
                tree_item['data'] = {'description': child.description}
            else:
                tree_item['text'] = item
                tree_item['children'] = child.as_treeview()
            metrics.append(tree_item)
        return metrics

    def generate_yaml(self, yaml_object, comment_indent):
        for item in self.__dict__.keys():
            child = self.__getattribute__(item)
            if type(child) == Description:
                yaml_object.yaml_add_eol_comment(child.description, child.id,
                                                 comment_indent)
            else:
                child.generate_yaml(yaml_object[item], comment_indent)

    def set_config(self, config: dict):
        for key in config:
            for item in self.__dict__.keys():
                child = self.__getattribute__(item)
                if type(child) == Description:
                    if child.id == key:
                        child.enabled = config[key]

                else:
                    if item == key:
                        child.set_config(config[key])

    def metrics_as_list(self, metric_list: list):
        for item in self.__dict__.keys():
            child = self.__getattribute__(item)
            if type(child) == Description:
                metric_list.append(child)
            else:
                child.metrics_as_list(metric_list)
