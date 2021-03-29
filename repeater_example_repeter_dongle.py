import time
from bleuio_lib.bleuio_funcs import BleuIo

repeter_dongle_port = "COM74"

repeter_dongle = BleuIo(port=repeter_dongle_port)
repeter_dongle.start_daemon()

buffer = ""
num_of_connected_devices = 0
connection_list = []

print("Dongle Connected.")

print(repeter_dongle.at_dual())
print(repeter_dongle.at_advstart())
repeter_dongle.rx_state = "rx_waiting"


def send_msg(buffer):
    result = buffer
    result_array1 = result.split("\r\n")
    dongle_sending_msg = result_array1[1]
    dongle_conn_idx = dongle_sending_msg.split("=")
    dongle_conn_idx = dongle_conn_idx[1].strip(")")
    print(dongle_sending_msg)
    print(dongle_conn_idx)
    result_array = result_array1[2].split(" ")
    msg_to_send = result_array[1]
    print(msg_to_send)
    time.sleep(0.1)
    target_conn = repeter_dongle.at_target_conn()
    target_conn = target_conn[0].split("=")
    target_conn = target_conn[1]
    print(target_conn)
    repeter_dongle.rx_state = "rx_waiting"
    if not msg_to_send == "":
        for conn in connection_list:
            if not conn == dongle_conn_idx:
                if not conn == target_conn:
                    repeter_dongle.at_target_conn(conn)
                    time.sleep(0.1)
                    repeter_dongle.rx_state = "rx_waiting"
                    time.sleep(0.1)
                repeter_dongle.at_spssend(msg_to_send)
                time.sleep(0.1)
                repeter_dongle.rx_state = "rx_waiting"


try:
    while 1:
        buffer = repeter_dongle.rx_buffer.decode("utf-8", "ignore")
        if "\r\nCONNECTED." in buffer:
            if "handle_evt_gap_connected: conn_idx=" in buffer:
                new_conn_inx = buffer
                new_conn_inx = new_conn_inx.split("\r\n")
                for line in new_conn_inx:
                    if "handle_evt_gap_connected: conn_idx=" in line:
                        c_idx = line.split(" ")
                        # print(c_idx)
                        c_idx = c_idx[1].split("=")
                        c_idx = c_idx[1]
                        print("CONN_INDEX=" + c_idx)
                        connection_list.append(c_idx)
                        print("connection_list=")
                        print(connection_list)
                        # print(line)
            num_of_connected_devices = num_of_connected_devices + 1
            print("ANOTHER DONGLE HAVE CONNECTED!")
            repeter_dongle.at_advstart()
            repeter_dongle.rx_state = "rx_waiting"
        if "\r\nDISCONNECTED." in buffer:
            num_of_connected_devices = num_of_connected_devices - 1
            connection_list = []
            print("NO CONNECTIONS.")
        if "\r\nconn_idx=" in buffer:
            for conn in connection_list:
                if "\r\nconn_idx=" + conn + " DISCONNECTED.\r\n" in buffer:
                    connection_list.remove(conn)
                    num_of_connected_devices = num_of_connected_devices - 1
                    print("DONGLE=" + conn + " DISCONNECTED.")
        if num_of_connected_devices > 0:
            if "\r\n[Received]:" in buffer:
                send_msg(buffer)
                # buffer = repeter_dongle.rx_buffer.decode("utf-8", "ignore")
        buffer = ""
        time.sleep(0.1)
except:
    repeter_dongle.at_advstop()
    repeter_dongle.at_gapdisconnect()
    print("Shutting down script.")