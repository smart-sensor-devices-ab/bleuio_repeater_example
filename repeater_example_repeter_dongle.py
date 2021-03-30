import time
from bleuio_lib.bleuio_funcs import BleuIo

repeter_dongle_port = "COM39"

repeter_dongle = BleuIo(port=repeter_dongle_port)
repeter_dongle.start_daemon()

buffer = ""
num_of_connected_devices = 0
connection_list = []

print("Dongle found.")

repeter_dongle.at_gapdisconnect()
repeter_dongle.at_dual()
repeter_dongle.at_advstart()
repeter_dongle.rx_state = "rx_waiting"
print("Waiting for other dongles to connect...")


def send_msg(buffer):
    try:
        result = buffer
        result_array1 = result.split("\r\n")
        dongle_sending_msg = result_array1[1]
        dongle_conn_idx = dongle_sending_msg.split("=")
        dongle_conn_idx = dongle_conn_idx[1].strip(")")
        result_array = result_array1[2].split(" ")
        msg_to_send = result_array[1]
        print("Forwarding data to reciever:")
        print(msg_to_send)
        if not msg_to_send == "":
            repeter_dongle.at_spssend(msg_to_send)
            repeter_dongle.rx_state = "rx_waiting"
    except:
        print(".")


try:
    while 1:
        buffer = repeter_dongle.rx_buffer.decode("utf-8", "ignore")
        if "\r\nCONNECTED." in buffer:
            num_of_connected_devices = num_of_connected_devices + 1
            print("A Dongle has connected!")
            repeter_dongle.at_advstart()
            repeter_dongle.rx_state = "rx_waiting"
        if "\r\nDISCONNECTED." in buffer:
            num_of_connected_devices = num_of_connected_devices - 1
            connection_list = []
            print("No Dongles connected.")
        if "\r\nconn_idx=" in buffer:
            for conn in connection_list:
                if "\r\nconn_idx=" + conn + " DISCONNECTED.\r\n" in buffer:
                    connection_list.remove(conn)
                    num_of_connected_devices = num_of_connected_devices - 1
                    print("A Dongle has disconnected!")
        if num_of_connected_devices > 1:
            if "\r\n[Received]:" in buffer:
                send_msg(buffer)
                buffer = ""
        time.sleep(0.1)
except KeyboardInterrupt:
    repeter_dongle.at_advstop()
    repeter_dongle.at_gapdisconnect()
    print("Shutting down script.")