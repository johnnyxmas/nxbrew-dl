import yaml


class DumperEdit(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(DumperEdit, self).increase_indent(flow, False)

    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()


def load_yml(f):
    """Load YAML file"""

    with open(f, "r") as file:
        config = yaml.safe_load(file)

    return config


def save_yml(f, data):
    """Save YAML file"""

    with open(f, "w") as file:
        yaml.dump(
            data,
            file,
            Dumper=DumperEdit,
            default_flow_style=False,
            sort_keys=False,
            indent=2,
        )
