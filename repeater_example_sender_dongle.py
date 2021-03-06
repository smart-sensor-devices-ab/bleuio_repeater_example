import time
from bleuio_lib.bleuio_funcs import BleuIo
import random

sender_dongle_port = "COM73"  # Change this to your dongle's COM port
mac_addr_to_repeater = (
    "[0]40:48:FD:E5:2D:74"  # Change this to your repeater dongle's mac address
)

sender_dongle = BleuIo(port=sender_dongle_port)
sender_dongle.start_daemon()

connected = False
data = ""
buffer = ""


def scan_and_get_results():
    """
    Starts a BLE scan for three seconds, looking for results including the 'FF' flag in the advertising data.
    Then it saves the results in a list and returns one of the results as a string.
    :return: string
    """
    print("Scanning...")
    return_data = ""
    result_list = []
    time.sleep(0.5)
    try:
        scanning = sender_dongle.at_findscandata("FF")
        if "SCANNING" in scanning[0]:
            time.sleep(4)
            sender_dongle.stop_scan()
            time.sleep(0.5)
            result_list = sender_dongle.rx_scanning_results
            if not result_list == []:
                if len(result_list) > 3:
                    lines = result_list[2].split("\r\n")
                    if not lines[1] == "":
                        data_array = lines[1].split(" ")
                        lenght = len(data_array)
                        if lenght == 5:
                            data = data_array[4]
                            return_data = data
            else:
                sender_dongle.stop_scan()
                result_list = []
                sender_dongle.rx_state = "rx_waiting"
                return_data = ""
    except:
        sender_dongle.stop_scan()
        result_list = []
        sender_dongle.rx_state = "rx_waiting"
        return_data = ""
    return return_data


print("Dongle found.")

try:
    sender_dongle.at_dual()
    ready = input(
        "Press enter to connect to the repeater dongle. (This should be connected last)."
    )
    print("Connecting...")
    sender_dongle.at_gapconnect(mac_addr_to_repeater)
    time.sleep(5)
    while not connected:
        connected_status = sender_dongle.ati()
        if "\r\nConnected" in connected_status[0]:
            connected = True
            break
        if "\r\nNot Connected" in connected_status[0]:
            sender_dongle.at_gapconnect(mac_addr_to_repeater)
            time.sleep(5)
        print("Trying to connect...")
        time.sleep(2)

    print("Connected.")
    print("Getting services...")
    get_services = sender_dongle.at_get_services()
    sender_dongle.rx_state = "rx_waiting"
    time.sleep(2)
    ready = input("Press enter to start sending data to the repeater dongle.")

    while 1:
        data = scan_and_get_results()
        time.sleep(1)
        if not data == "":
            sent = sender_dongle.at_spssend(data)
            time.sleep(0.1)
            if len(sent) == 1:
                if "[Sent]" in sent[0]:
                    print("Data = (" + data + ") sent.")
                    time.sleep(1)
            data = ""
        time.sleep(1)
        sender_dongle.rx_state = "rx_waiting"
except KeyboardInterrupt:
    sender_dongle.at_gapdisconnect()
    print("Shutting down script.")