#from fastapi import FastAPI, WebSocket
#from fastapi.responses import HTMLResponse
from paho.mqtt.reasoncodes import ReasonCode
from paho.mqtt.client import Client, MQTTMessage, Properties, ConnectFlags
from typing import Optional, Set
from .callbacks import on_connect, on_message, subscribe_callback, publish_callback
from  decouple import config
from paho.mqtt import client as mqtt_client
import time, logging

#------------REST API Stuff-------------------------------------

"""
These are active when the FastAPI server is called. 
"""
"""
app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json(mode='text')
        await websocket.send_text(f"Message text was: {data["ls"][4]}")
"""




#---------------MQTT CLIENT STUFF---------------------------
        
def mqttc(message: str=None) -> None:
    """
    Source for clients on MQTT system to run.

    Connects to broker, then receives messages on a forever loop
    """

    #diagnostics
    logging.basicConfig(level=logging.DEBUG)

    #create client instance
    client = Client(mqtt_client.CallbackAPIVersion.VERSION2, client_id="buster")
    client.enable_logger()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = subscribe_callback
    client.on_publish = publish_callback

    unp_pub = set()

    client.user_data_set(unp_pub)

    broker_host = config("HANNITY_IP")  
    broker_port = 1883
    username = config("HAOS_UNAME")  
    password = config("HAOS_PASS")  

    # Set username and password for authentication
    client.username_pw_set(username=username, password=password)

    client.connect(host=broker_host, port=broker_port)

    """
    HANNITY - Broker (Raspberry Pi on Home Assistant)
    MAC - Broker (My laptop)
    BUSTER - handles web server and electronic peripherals
    ADDIE/JET - handles motion sensor and camera
    """

    client.subscribe("topic/state")

    msg_info = client.publish("topic/state", "buster joined", qos=1)

    unp_pub.add(msg_info.mid)

    while len(unp_pub):
        time.sleep(0.1)

    # solution to race-condition problem
    msg_info.wait_for_publish()


    if message != None:
        main_msg = client.publish("topic/state", message, qos=1)
        unp_pub.add(main_msg.mid)
        while len(unp_pub):
            time.sleep(0.1)
        
        main_msg.wait_for_publish()


    client.loop_forever()



"""
connect(host: str, port: int = 1883, 
        keepalive: int = 60, bind_address: str = '', 
        bind_port: int = 0, clean_start: bool | Literal[3] = 3, 
        properties: Properties | None = None)
"""

if __name__ == "__main__":
    mqttc()

