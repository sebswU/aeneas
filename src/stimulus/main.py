from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from paho.mqtt.reasoncodes import ReasonCode
from paho.mqtt.client import Client, MQTTMessage, Properties, ConnectFlags
from  decouple import config
from paho.mqtt import client as mqtt_client
import time

#------------REST API Stuff-------------------------------------

"""
These are active when the FastAPI server is called. 
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

#---------------MQTT CLIENT STUFF---------------------------
        
def mqttc(args=None, helpers=None) -> None:
    """
    Source for clients on MQTT system to run.

    Connects to broker, then receives messages on a forever loop
    """
    client = Client(mqtt_client.CallbackAPIVersion.VERSION2, client_id="buster")
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = subscribe_callback
    client.on_publish = publish_callback

    unp_pub = set()

    client.user_data_set(unp_pub)
    client.connect("127.0.0.1",port=1883) 
    """
    client.connect(host=config("BUSTER_IP"),port=1883)
    """

    client.loop_start()


    #client.subscribe("topic/state")

    msg_info = client.publish("topic/state", "hello world", qos=1)
    unp_pub.add(msg_info.mid)

    msg_info_2 = client.publish("topic/state", "hello world 2", qos=1)
    unp_pub.add(msg_info_2.mid)

    while len(unp_pub):
        time.sleep(0.1)

    # solution to race-condition problem
    msg_info.wait_for_publish()
    msg_info_2.wait_for_publish()

    client.disconnect()
    client.loop_stop()



def on_connect(client: Client, userdata, 
               flags: ConnectFlags, reason_code: ReasonCode,
               properties: Properties) -> None:
    """Success affirmation prints to console if connected to BROKER"""

    if flags.session_present:
        print("Session is present")
    if reason_code == 0:
        print(f"Connected with result code {reason_code}")
    if reason_code > 0:
        print("There has been an error processing the MQTT request")
        print(f"reason code: {reason_code}")




def on_message(client: Client, userdata, message: MQTTMessage) -> None:
    """Affirmation of getting message and printing said message to console"""
    print("got message")

    #message.payload is sent in bytes, so must decode to UTF-8 format (default)
    print(message.payload.decode())



def subscribe_callback(client: Client, userdata, 
                       mid: int, reason_code_list: list[ReasonCode], 
                       properties: Properties) -> None:
    """Affirmation of subscription to topic"""

    for sub in reason_code_list:
        if sub == 1:
            print("process QoS = 1")
        if sub >= 128:
            print(f"Failure, reason code {sub}: error processing")
        if reason_code_list[0] >= 128:
            print(f"Error: reason code {sub}")
        


def publish_callback(client: Client, userdata, 
                     mid: int, reason_code: ReasonCode, 
                     properties: Properties) -> None:
    """Affirmation of published message to console"""
    try:
        userdata.remove(mid)
    except KeyError:
        print("on_publish() is called with a mid not present in unacked_publish")
        print("This is due to an unavoidable race-condition:")
        print("* publish() return the mid of the message sent.")
        print("* mid from publish() is added to unacked_publish by the main thread")
        print("* on_publish() is called by the loop_start thread")
        print("While unlikely (because on_publish() will be called after a network round-trip),")
        print(" this is a race-condition that COULD happen")
        print("")
        print("The best solution to avoid race-condition is using the msg_info from publish()")
        print("We could also try using a list of acknowledged mid rather than removing from pending list,")
        print("but remember that mid could be re-used !")


    print(f"published to topic with reason code {reason_code}")








"""
connect(host: str, port: int = 1883, 
        keepalive: int = 60, bind_address: str = '', 
        bind_port: int = 0, clean_start: bool | Literal[3] = 3, 
        properties: Properties | None = None)
"""

if __name__ == "__main__":
    mqttc()

