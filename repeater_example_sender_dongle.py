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
connected_devices = 0
scanning = False
recieved_message = ""


def get_scan_results(buffer):
    try:
        return_data = ""
        line_array = buffer.split("\r\n")
        word_array = line_array[1].split(" ")
        if len(word_array) == 5:
            return_data = word_array[4]
        else:
            return_data = ""

        return return_data
    except:
        return ""


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
    console.write("\r".encode())
    time.sleep(0.1)
    ready = input(
        "Press enter to connect to the repeater dongle. (This should be connected last)."
    )
    console.write(str.encode("AT+GAPCONNECT="))
    console.write(mac_addr_to_repeater.encode())
    console.write("\r".encode())
    time.sleep(0.1)
    print("Connecting...")
    while not connected:
        try:
            dongle_output = console.read(console.in_waiting)
        except:
            dongle_output = " "
        time.sleep(0.5)
        if not dongle_output.isspace():
            if dongle_output.__contains__(str.encode("\r\nCONNECTED.\r\n")):
                connected = True
                print("Connected!")
                ready2 = input(
                    "Press enter to start scanning and sending data to the repeater dongle."
                )
                console.write(str.encode("AT+FINDSCANDATA=5B070503"))
                console.write("\r".encode())
                scanning = True
            if dongle_output.__contains__(str.encode("DISCONNECTED.")):
                print("Lost the connection.")
                connected = False
            dongle_output = " "
    while connected:
        dongle_output = console.read(console.in_waiting)
        time.sleep(0.5)
        if not dongle_output.isspace():
            if dongle_output.__contains__(str.encode("SCANNING")):
                print("Scanning...")
                scanning = True
            if dongle_output.__contains__(str.encode("SCAN COMPLETE")):
                print("Stopped scanning...")
                scanning = False
            if dongle_output.__contains__(str.encode("Device Data")):
                recieved_message = get_scan_results(
                    dongle_output.decode("utf-8", "ignore")
                )
                if not recieved_message == "":
                    time.sleep(0.5)
                    console.write("\x03".encode())
            if not recieved_message == "":
                try:
                    print("Data = (" + recieved_message + ") sent.")
                    console.write(str.encode("AT+SPSSEND="))
                    console.write(recieved_message.encode())
                    time.sleep(0.1)
                    console.write("\r".encode())
                    time.sleep(3)
                    recieved_message = ""
                    time.sleep(1)
                    console.write(str.encode("AT+FINDSCANDATA=5B070503"))
                    time.sleep(0.1)
                    console.write("\r".encode())
                    time.sleep(0.5)
                except:
                    time.sleep(0.1)
            if dongle_output.__contains__(str.encode("DISCONNECTED.")):
                print("Lost the connection.")
                connected = False
            dongle_output = ""