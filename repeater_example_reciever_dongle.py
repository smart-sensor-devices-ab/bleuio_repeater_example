import time
from bleuio_lib.bleuio_funcs import BleuIo

dongle3_port = "COM77"
mac_addr_to_dongle2 = "[0]40:48:FD:E5:2D:3A"

buffer = ""

dongle3 = BleuIo(port=dongle3_port)
dongle3.start_daemon()


def save_msg(buffer):
    result = buffer
    result_array1 = result.split("\r\n")
    result_array = result_array1[2].split(" ")
    msg_to_save = str(result_array[0])
    print("Recieved =" + msg_to_save)


try:
    dongle3.at_dual()
    ready = input("Press enter when you started the other scripts.")
    dongle3.at_gapconnect(mac_addr_to_dongle2)

    while 1:
        buffer = dongle3.rx_buffer.decode("utf-8", "ignore")
        if "\r\nhandle_evt_gattc_notification:" in buffer:
            save_msg(buffer)
        if not buffer == "":
            print(buffer)
            buffer = ""
        time.sleep(0.1)
except:
    dongle3.at_gapdisconnect()
    print("Shutting down script.")