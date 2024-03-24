import serial
import io
import serial.tools.list_ports


class GCodeGenerator:

    def __init__(self):
        self.ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(self.ports):
            print(f"{port}: {desc} [{hwid}]")

        ###########################################################
        # commented out for testing without the serial connection
        ###########################################################
        # self.port = self.ports[0]
        # self.g_code = ""
        # self.g_code_list = []
        # self.g_code_list_index = 0
        # self.g_code_list_length = 0
        # self.serial_port = serial.Serial(port, 9600, timeout=1)
        # self.serial_port.flush()

    def setGCode(self, g_code):
        self.g_code = g_code
        self.g_code_list = g_code.split("\n")
        self.g_code_list_length = len(self.g_code_list)
        self.g_code_list_index = 0
        if self.g_code_list_length > 0:
            self.sendGCode()
        else:
            print("No G-Code to send")

    def sendGCode(self):
        print("Sending G-Code")
        self.serial_port.write(self.g_code_list[self.g_code_list_index].encode())
        print(self.g_code_list[self.g_code_list_index])
        self.g_code_list_index += 1
        count = 0;
        out=""
        while self.serial_port.readline().decode():
            if self.serial_port.readline() != b"OK\n":
                print(self.serial_port.readline().decode())
            else:
                self.serial_port.write(self.g_code_list[self.g_code_list_index].encode())
                print(self.g_code_list[self.g_code_list_index])
                self.g_code_list_index += 1
                count += 1

            if self.g_code_list_index >= self.g_code_list_length:
                break

    def sendHoming(self):
        self.serial_port.write(b"G28\n")
