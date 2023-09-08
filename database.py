from peewee import *
import yaml

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

user = config['db']['username']
password = config['db']['password']
db_name = config['db']['db_name']

conn = MySQLDatabase(
    db_name, user=user,
    password=password,
    host=config['db']['host']
)
