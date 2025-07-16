import sys
import os
import unittest
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from stimulus.callbacks import Client, MQTTMessage, Properties, ConnectFlags

def test_mqtt_client():
    from stimulus.client import mqtt_client

    assert mqtt_client is not None

def test_client_initialization():
    client = Client(client_id="test_client")
    assert client is not None
    assert client._client_id == "test_client"


def test_client_connect_and_publish():
    client = Client(client_id="test_client")
    client.connect("localhost", 1883, 60)
    
    # Mock a publish to test the method
    result = client.publish("test/topic", "test message")
    
    assert result.rc == 0  # Assuming 0 means success
    assert result.mid is not None  # Message ID should be set
    assert isinstance(result.properties, Properties)  # Properties should be an instance of Properties