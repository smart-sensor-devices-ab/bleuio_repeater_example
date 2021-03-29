import time
from bleuio_lib.bleuio_funcs import BleuIo

dongle1_port = "COM73"
mac_addr_to_dongle2 = "[0]40:48:FD:E5:2D:3A"

dongle1 = BleuIo(port=dongle1_port)
dongle1.start_daemon()

data = ""
buffer = ""


def save_msg(buffer):
    result = buffer
    result_array1 = result.split("\r\n")
    # print(result_array1)
    result_array = result_array1[2].split(" ")
    # print(result_array)
    msg_to_save = str(result_array[0])
    print("SAVED=" + msg_to_save)


print("Dongle Connected.")

try:
    print(dongle1.at_dual())
    dongle1.rx_state = "rx_waiting"
    ready = input("Press enter when you started the other scripts.")
    dongle1.at_gapconnect(mac_addr_to_dongle2)
    dongle1.rx_state = "rx_waiting"
    time.sleep(3)
    while 1:
        buffer = dongle1.rx_buffer.decode("utf-8", "ignore")
        if "\r\nhandle_evt_gattc_notification:" in buffer:
            save_msg(buffer)
        print(dongle1.at_findscandata("FF5B07"))
        time.sleep(3)
        dongle1.stop_scan()
        time.sleep(0.5)
        result_list = dongle1.rx_scanning_results
        if not result_list == []:
            for results in result_list:
                lines = results.split("\r\n")
                for line in lines:
                    if not line == "":
                        data_array = line.split(" ")
                        lenght = len(data_array)
                        if lenght == 5:
                            data = data_array[4]
                            print(data)
                            break
                            # if "B0032" in data:
                            #     print(data)
        else:
            dongle1.stop_scan()
            dongle1.rx_state = "rx_waiting"
        time.sleep(2)
        if not data == "":
            print(dongle1.at_spssend(data))
            dongle1.rx_state = "rx_waiting"
            data = ""
        print("Loop.")
        if not buffer == "":
            print(buffer)
            buffer = ""
        time.sleep(0.1)
except:
    dongle1.stop_scan()
    dongle1.rx_state = "rx_waiting"
    dongle1.at_gapdisconnect()
    dongle1.rx_state = "rx_waiting"
    print("Shutting down script.")