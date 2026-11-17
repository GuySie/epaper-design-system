"""YAML for page definitions and generated blueprints: `!input name` kept as a tag, multi-line text as a literal block,
keys in the order they were given."""
import yaml


class Input(dict):
    """{'!input': name} as loaded; written back as `!input name`"""


class Loader(yaml.SafeLoader):
    pass


Loader.add_constructor('!input', lambda l, n: Input({'!input': l.construct_scalar(n)}))


class Dumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def _str(d, s):
    if '\n' in s:
        return d.represent_scalar('tag:yaml.org,2002:str', s, style='|')
    return d.represent_scalar('tag:yaml.org,2002:str', s)


def _dict(d, m):
    if set(m) == {'!input'} and isinstance(m['!input'], str):
        return d.represent_scalar('!input', m['!input'])
    return d.represent_mapping('tag:yaml.org,2002:map', m.items())


Dumper.add_representer(str, _str)
Dumper.add_representer(dict, _dict)
Dumper.add_representer(Input, _dict)


def load(text):
    return yaml.load(text, Loader=Loader)


def dump(data, width=120):
    return yaml.dump(data, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=width, default_flow_style=False)
