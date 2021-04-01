import time
import serial

your_com_port = "COM38"  # Change this to the com port your dongle is connected to.

# Global
connecting_to_dongle = True
dongle_output = ""
connected = False
connected_devices = 0


def send_msg(buffer):
    """
    Parses incomming data string for just the data.
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
        return msg_to_send
    except:
        print(" ")


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
# Making sure the dongle is not connected on startup. Running twice in case both dongles are connected.
console.write(str.encode("AT+GAPDISCONNECT"))
time.sleep(0.1)
console.write("\r".encode())
time.sleep(0.1)
console.write(str.encode("AT+GAPDISCONNECT"))
time.sleep(0.1)
console.write("\r".encode())


while 1 and console.is_open.__bool__():
    print("Starting advertising.")
    time.sleep(0.1)
    console.write(str.encode("AT+DUAL"))
    time.sleep(0.1)
    console.write("\r".encode())
    time.sleep(0.1)
    console.write(str.encode("AT+ADVSTART"))
    time.sleep(0.1)
    console.write("\r".encode())
    time.sleep(0.1)
    print("Awaiting connections...")
    while not connected:
        dongle_output = console.read(console.in_waiting)
        time.sleep(0.5)
        if not dongle_output.isspace():
            if dongle_output.__contains__(str.encode("\r\nCONNECTED.\r\n")):
                connected_devices = connected_devices + 1
                if connected_devices > 1:
                    connected = True
                print("Connected!")
                console.write(str.encode("AT+ADVSTART"))
                time.sleep(0.1)
                console.write("\r".encode())
            if dongle_output.__contains__(str.encode("DISCONNECTED.")):
                print("Lost a connection.")
                connected_devices = connected_devices - 1
                connected = False
            dongle_output = " "
    while connected:
        dongle_output = console.read(console.in_waiting)
        time.sleep(0.5)
        if not dongle_output.isspace():
            if dongle_output.__contains__(str.encode("\r\n[Received]: ")):
                recieved_message = send_msg(dongle_output.decode("utf-8", "ignore"))
                if not recieved_message == "":
                    console.flush()
                    time.sleep(0.2)
                    print("Forwarding data to reciever:")
                    print(recieved_message)
                    console.write(str.encode("AT+SPSSEND="))
                    console.write(recieved_message.encode())
                    time.sleep(0.1)
                    console.write("\r".encode())
                    time.sleep(0.2)
            if dongle_output.__contains__(str.encode("DISCONNECTED.")):
                print("Lost a connection.")
                connected_devices = connected_devices - 1
                connected = False
            dongle_output = ""