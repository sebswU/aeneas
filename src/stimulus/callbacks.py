from paho.mqtt.reasoncodes import ReasonCode
from paho.mqtt.client import Client, MQTTMessage, Properties, ConnectFlags


from decouple import config
import time, logging
from typing import Optional, Set
from paho.mqtt import client as mqtt_client



def on_connect(client: Client, userdata: Optional[Set[str]], flags: ConnectFlags, rc: ReasonCode) -> None:
    """
    Callback function for when the client connects to the MQTT broker.
    """
    logging.info(f"Connected with result code {rc}")
    if rc == ReasonCode.SUCCESS:
        client.subscribe("home/+/status")
        logging.info("Subscribed to home/+/status")
    else:
        logging.error(f"Failed to connect, return code {rc}")

def on_message(client: Client, userdata: Optional[Set[str]], message: MQTTMessage) -> None:
    """
    Callback function for when a message is received from the MQTT broker.
    """
    logging.info(f"Received message '{message.payload.decode()}' on topic '{message.topic}'")
    # Here you can add logic to handle the received message
    # For example, you could parse the message and update some state or trigger actions

def on_subscribe(client: Client, userdata: Optional[Set[str]], mid: int, granted_qos: list[ReasonCode]) -> None:
    """
    Callback function for when the client subscribes to a topic.
    """
    logging.info(f"Subscribed with mid {mid} and QoS {granted_qos}")
    if granted_qos[0] == ReasonCode.SUCCESS:
        logging.info("Subscription successful")
    else:
        logging.error(f"Subscription failed with reason code {granted_qos[0]}")

def on_publish(client: Client, userdata: Optional[Set[str]], mid: int, reason_code: ReasonCode) -> None:
    """
    Callback function for when a message is published to the MQTT broker.
    """
    logging.info(f"Message published with mid {mid} and reason code {reason_code}")
    if reason_code != ReasonCode.SUCCESS:
        logging.error(f"Publish failed with reason code {reason_code}")