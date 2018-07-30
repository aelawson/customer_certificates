import yaml
import os

env = os.environ.get('env', 'lcl')

with open('config.yaml') as conf:
    conf_base = yaml.safe_load(conf)

Config = conf_base.get(env, conf_base['lcl'])
