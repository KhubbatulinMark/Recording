import logging
import datetime
import os
import sys
from pathlib import Path
from configparser import ConfigParser

BASE_PATH = Path(__file__).parent

sys.path.append(str(BASE_PATH))


def parse_config(config_name: str, base_path: Path = BASE_PATH) -> ConfigParser:
    """Считывание конфигурационного файла"""
    config = ConfigParser(
        converters={
            "datetime": lambda s:
            datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')
        }
    )
    config_path = base_path.joinpath(config_name)

    if config_path.is_file() and os.access(config_path.absolute(), os.R_OK):
        config.read(config_path.absolute())
        print(f'Using configs in {config_path}')
    else:
        if os.path.isfile(config_name):
            error = "not accessible"
        else:
            error = f"doesn't exist in {base_path.absolute()}"

        print((f"The {config_name} {error}. Please use {config_name}.example "
               f"to create new {config_name} file"))
        sys.exit(1)

    return config


config_name = 'config.ini'
config = parse_config(config_name)

# clickhouse-telemetry
CH_TELEMETRY_URL = config['clickhouse-telemetry']['URL']
CH_TELEMETRY_DATABASE = config['clickhouse-telemetry']['DATABASE']
CH_TELEMETRY_TABLE_NAME = config['clickhouse-telemetry']['TABLE_NAME']
CH_TELEMETRY_USER = config['clickhouse-telemetry']['USER']
CH_TELEMETRY_PASSWORD = config['clickhouse-telemetry']['PASSWORD']

# clickhouse-math
CH_MATH_URL = config['clickhouse-math']['URL']
CH_MATH_DATABASE = config['clickhouse-math']['DATABASE']
CH_MATH_TABLE_NAME = config['clickhouse-math']['TABLE_NAME']
CH_MATH_USER = config['clickhouse-math']['USER']
CH_MATH_PASSWORD = config['clickhouse-math']['PASSWORD']

# postgres-events
EVENTS_HOST = config['postgres-events']['HOST']
EVENTS_PORT = config['postgres-events']['PORT']
EVENTS_DATABASE = config['postgres-events']['DATABASE']
EVENTS_TABLE_NAME = config['postgres-events']['TABLE_NAME']
EVENTS_USER = config['postgres-events']['USER']
EVENTS_PASSWORD = config['postgres-events']['PASSWORD']

# 1C
SYSTEM_1C_WSDL_URL = config['1c']['WSDL_URL']
RULE_1_MSG = config['1c']['RULE_1_MSG']
RULE_2_MSG = config['1c']['RULE_2_MSG']

# row counts in one insert
ETL_CHUNK_SIZE = config['general'].getint('ETL_CHUNK_SIZE')
MATH_CHUNK_SIZE = config['general'].getint('MATH_CHUNK_SIZE')
EVENTS_CHUNK_SIZE = config['general'].getint('EVENTS_CHUNK_SIZE')

MODBUS_PORT = config['modbus'].get('PORT')
MODBUS_TIMEOUT = config['modbus'].getfloat('TIMEOUT')

TURN_OFF_TEMP = config['modbus'].getfloat('TURN_OFF_TEMP')

# math
ROOM_TEMP = config['math'].getint('ROOM_TEMP')

# setup logging
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
cf = logging.FileHandler('modbus-adapter.log')
logging.basicConfig(format='%(asctime)s %(message)s',
                    level=logging.INFO,
                    handlers=[ch, cf])

# RABBIT
HOST = 'localhost'
EXCHANGE = 'telemetry'
EXCHANGE_EVENTS = 'events'

ENTITY_ID_1 = config['platform'].getint('ENTITY_ID_1')
ENTITY_ID_2 = config['platform'].getint('ENTITY_ID_2')
SERIES_STORAGE_TELEMETRY = config['platform'].getint('SERIES_STORAGE_TELEMETRY')
SERIES_STORAGE_MATH = config['platform'].getint('SERIES_STORAGE_MATH')