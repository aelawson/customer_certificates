import yaml
import os

env = os.environ.get('env', 'local')

with open('config.yaml') as conf:
    conf_base = yaml.safe_load(conf)

try:
    Config = conf_base[env]
except KeyError:
    raise Exception('Invalid environment! Make sure your $env var is set properly.')