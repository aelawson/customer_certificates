import yaml
import os

env = os.environ.get('env', 'local')

with open('config.yaml') as conf:
    conf_base = yaml.safe_load(conf)

if env not in conf_base['envs']:
    raise Exception("""
        Invalid environment!
        Make sure your env is correct and listed in the config envs section.
        \n
    """)

Config = conf_base[env]