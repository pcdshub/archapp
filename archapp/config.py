"""
config.py defines default archive appliance server properties
"""
import os

hostname = os.environ.get("ARCHAPP_HOSTNAME", "pscaa02")
data_port = int(os.environ.get("ARCHAPP_DATA_PORT", 17668))
mgmt_port = int(os.environ.get("ARCHAPP_MGMT_PORT", 17665))
