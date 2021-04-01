import time
import serial

your_com_port = "COM71"  # Change this to the com port your dongle is connected to.
mac_addr_to_repeater = (
    "[0]40:48:FD:E5:2D:74"  # Change this to your repeater dongle's mac address
)

# Global
connecting_to_dongle = True
dongle_output = ""
connected = False
recieved_message = ""


def save_msg(buffer):
    """
    Parses incomming data string for just the data and prints it out.
    """
    result = buffer
    result_array1 = result.split("\r\n")
    result_array = result_array1[2].split(" ")
    msg_to_save = str(result_array[0])
    print("Recieved = " + msg_to_save)


print("Connecting to dongle...")
while connecting_to_dongle:
    try:
        console = serial.Serial(
            port=your_com_port,
            baudrate=57600,
            parity="N",
            stopbits=1,
            bytesize=8,
            timeout=0,
        )
        if console.is_open.__bool__():
            connecting_to_dongle = False
    except:
        print("Dongle not connected. Please reconnect Dongle.")
        time.sleep(5)

print("\n\nFound the Dongle.\n")


while 1 and console.is_open.__bool__():
    time.sleep(0.1)
    console.write(str.encode("AT+DUAL"))
    time.sleep(0.1)
    console.write("\r".encode())
    time.sleep(0.1)
    ready = input(
        "Press enter to connect to the repeater dongle. (This should be connected first)."
    )
    console.write(str.encode("AT+GAPCONNECT="))
    console.write(mac_addr_to_repeater.encode())
    time.sleep(0.1)
    console.write("\r".encode())
    time.sleep(0.1)
    print("Connecting...")
    while not connected:
        dongle_output = console.read(console.in_waiting)
        time.sleep(0.5)
        if not dongle_output.isspace():
            if dongle_output.__contains__(str.encode("\r\nCONNECTED.\r\n")):
                connected = True
                print("Connected!")
                time.sleep(3)
            if dongle_output.__contains__(str.encode("DISCONNECTED.")):
                print("Lost the connection.")
                connected = False
                break
            dongle_output = " "
    while connected:
        dongle_output = console.read(console.in_waiting)
        time.sleep(0.5)
        if not dongle_output.isspace():
            if dongle_output.__contains__(
                str.encode("\r\nhandle_evt_gattc_notification:")
            ):
                save_msg(dongle_output.decode("utf-8", "ignore"))
            if dongle_output.__contains__(str.encode("DISCONNECTED.")):
                print("Lost the connection.")
                connected = False
            dongle_output = ""