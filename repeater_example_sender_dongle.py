import time
from bleuio_lib.bleuio_funcs import BleuIo
import random

sender_dongle_port = "COM38"
mac_addr_to_repeater = "[0]40:48:FD:E5:2D:9C"

sender_dongle = BleuIo(port=sender_dongle_port)
sender_dongle.start_daemon()

connected = False
data = ""
buffer = ""

print("Dongle found.")

try:
    sender_dongle.at_dual()
    sender_dongle.rx_state = "rx_waiting"
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
        # print(sender_dongle.at_findscandata("FF5B07"))
        # time.sleep(3)
        # sender_dongle.stop_scan()
        # time.sleep(0.5)
        # result_list = sender_dongle.rx_scanning_results
        # if not result_list == []:
        #     for results in result_list:
        #         lines = results.split("\r\n")
        #         for line in lines:
        #             if not line == "":
        #                 data_array = line.split(" ")
        #                 lenght = len(data_array)
        #                 if lenght == 5:
        #                     data = data_array[4]
        #                     print(data)
        #                     break
        # else:
        #     sender_dongle.stop_scan()
        #     sender_dongle.rx_state = "rx_waiting"
        # time.sleep(2)
        data = "sender_data" + str(random.randint(0, 1000 - 1))
        if not data == "":
            sent = sender_dongle.at_spssend(data)
            sender_dongle.rx_state = "rx_waiting"
            if "[Sent]" in sent[0]:
                print("Data = (" + data + ") sent.")
            time.sleep(5)
            data = ""
        print("Loop.")
        time.sleep(0.1)
except KeyboardInterrupt:
    sender_dongle.at_gapdisconnect()
    print("Shutting down script.")