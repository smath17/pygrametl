# This file was generated by PygramETL-DeclarativeETL in conformity with a given specification.
# Credit Simon Mathiasen 2023 (AAU)

import psycopg2
import pygrametl
from pygrametl.datasources import SQLSource, CSVSource
from pygrametl.tables import CachedDimension, FactTable

dw_string = "host='localhost' dbname='test' user='postgres' password='1234'"
dw_conn = psycopg2.connect(dw_string)
dw_conn_wrapper = pygrametl.ConnectionWrapper(connection=dw_conn)

Customer_Dimension = CachedDimension(
    name='Customer_Dimension',
    key='CustomerKEY',
    attributes=['name', 'address'])

Part_Dimension = CachedDimension(
    name='Part_Dimension',
    key='PartKEY',
    attributes=['name', 'manufacturer'])

Date_Dimension = CachedDimension(
    name='Date_Dimension',
    key='DateKEY',
    attributes=['day', 'month', 'year'])

Lineorder_Fact_Table = FactTable(
    name='Lineorder_Fact_Table',
    keyrefs=['CustomerKEY', 'PartKEY', 'DateKEY'],
    measures=['quantity', 'price'])