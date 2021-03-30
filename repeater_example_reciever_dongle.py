import time
from bleuio_lib.bleuio_funcs import BleuIo

reciever_dongle_port = "COM74"
mac_addr_to_repeater = "[0]40:48:FD:E5:2D:9C"

buffer = ""
connected = False
connecting = ""

reciever_dongle = BleuIo(port=reciever_dongle_port)
reciever_dongle.start_daemon()

print("Dongle found.")


def save_msg(buffer):
    result = buffer
    result_array1 = result.split("\r\n")
    result_array = result_array1[2].split(" ")
    msg_to_save = str(result_array[0])
    print("Recieved = " + msg_to_save)


try:
    reciever_dongle.at_dual()
    ready = input(
        "Press enter to connect to the repeater dongle. (This should be connected first)."
    )
    print("Connecting...")
    reciever_dongle.at_gapconnect(mac_addr_to_repeater)
    time.sleep(5)
    while not connected:
        connected_status = reciever_dongle.ati()
        if "\r\nConnected" in connected_status[0]:
            connected = True
            break
        if "\r\nNot Connected" in connected_status[0]:
            reciever_dongle.at_gapconnect(mac_addr_to_repeater)
            time.sleep(5)
        print("Trying to connect...")
        time.sleep(2)

    print("Connected. Waiting to recieve...")

    while 1:
        buffer = reciever_dongle.rx_buffer.decode("utf-8", "ignore")
        if "\r\nhandle_evt_gattc_notification:" in buffer:
            save_msg(buffer)
        buffer = ""
        time.sleep(0.5)
except KeyboardInterrupt:
    reciever_dongle.at_gapdisconnect()
    print("Shutting down script.")