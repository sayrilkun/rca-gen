import logging
import os
import streamlit as st


import json
from azure.cosmos import CosmosClient, PartitionKey
#
# Setup
#
logging.basicConfig(level=logging.INFO, format="%(asctime)s|%(filename)s:%(lineno)d|%(funcName)s|%(message)s")

#
# Globals
#
log = logging.getLogger(__name__)

ENDPOINT = st.secrets.secrets["azure"]["endpoint"][0]
KEY = st.secrets.secrets["azure"]["key"][0]
DATABASE_NAME = "datamrkdb"
CONTAINER_NAME = "incidents"
client = CosmosClient(url=ENDPOINT, credential=KEY)
database = client.create_database_if_not_exists(id=DATABASE_NAME)

key_path = PartitionKey(path="/categoryId")
container = database.create_container_if_not_exists(
    id=CONTAINER_NAME, partition_key=key_path, offer_throughput=400
)
