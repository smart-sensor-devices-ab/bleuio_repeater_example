import time
from bleuio_lib.bleuio_funcs import BleuIo

repeter_dongle_port = "COM38"  # Change this to your dongle's COM port

repeter_dongle = BleuIo(port=repeter_dongle_port)
repeter_dongle.start_daemon()

buffer = ""
num_of_connected_devices = 0
connection_list = []

print("Dongle found.")

repeter_dongle.at_dual()
repeter_dongle.at_advstart()
repeter_dongle.rx_state = "rx_waiting"
print("Waiting for other dongles to connect...")


def send_msg(buffer):
    """
    Parses incomming data string for just the data and sends it forward via the Serial Port Service.
    """
    try:
        result = buffer
        msg_to_send = ""
        result_array1 = result.split("\r\n")
        for line in result_array1:
            if "[Received]:" in line:
                msg_to_send = line.split(" ")
                msg_to_send = msg_to_send[1]
                break
        print("Forwarding data to reciever:")
        print(msg_to_send)
        if not msg_to_send == "":
            repeter_dongle.at_spssend(msg_to_send)
            repeter_dongle.rx_state = "rx_waiting"
    except:
        print(" ")


try:
    while 1:
        buffer = repeter_dongle.rx_buffer.decode("utf-8", "ignore")
        if "\r\nCONNECTED." in buffer:
            num_of_connected_devices = num_of_connected_devices + 1
            print("A Dongle has connected!")
            repeter_dongle.at_advstart()
            repeter_dongle.rx_state = "rx_waiting"
        if "DISCONNECTED." in buffer:
            num_of_connected_devices = num_of_connected_devices - 1
            connection_list = []
            print("No Dongles connected.")
        if num_of_connected_devices > 1:
            if "\r\n[Received]:" in buffer:
                # print(buffer)
                send_msg(buffer)
        buffer = ""
        time.sleep(0.1)
except KeyboardInterrupt:
    repeter_dongle.at_advstop()
    repeter_dongle.at_gapdisconnect()
    print("Shutting down script.")