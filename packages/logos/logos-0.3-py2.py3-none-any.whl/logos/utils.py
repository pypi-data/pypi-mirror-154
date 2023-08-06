import os
import logging

from pathlib import Path
import yaml

ROOT_DIR = Path(os.path.realpath(__file__)).parents[1]
CONFIG_ENV = os.getenv('CONFIG_ENV')
CONFIG_PATH = ROOT_DIR / 'config' / f'{CONFIG_ENV}.yml'

with CONFIG_PATH.open(mode='r', encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
config['root_dir'] = ROOT_DIR
config['data_path'] = ROOT_DIR / 'data'


logging.basicConfig(level=config['log']['level'])
logger = logging.getLogger(__name__)
