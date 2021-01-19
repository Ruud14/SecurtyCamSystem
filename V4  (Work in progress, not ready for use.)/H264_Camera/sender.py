import socket
import os


class Sender:
    def __init__(self, storage_ip):
        self.storage_ip = storage_ip
        self.transfer_port = 5005

    # Sends the recorded file to server and deletes the file.
    def send_recording(self, file_path):
        if os.path.isfile(file_path):
            print("Sending Recording {} to {}.".format(file_path, self.storage_ip))
            s = socket.socket()
            s.settimeout(5)
            try:
                s.connect((self.storage_ip, self.transfer_port))
            except Exception as e:
                print(
                    "Sending recording failed,"
                    " Still removing the recording to prevent local storage from getting full. \n",
                    str(e))
                os.remove(file_path)
                return
            s.settimeout(None)
            s.send(("EXISTS" + str(os.path.getsize(file_path))).encode())
            print("FileSize: ", str(os.path.getsize(file_path)).encode())
            response = s.recv(1024)
            response = response.decode()
            if response.startswith('OK'):
                with open(file_path, 'rb') as f:
                    bytes_to_send = f.read(4096)
                    s.send(bytes_to_send)
                    while bytes_to_send != b"":
                        bytes_to_send = f.read(4096)
                        s.send(bytes_to_send)
            s.close()
            os.remove(file_path)
            print("File Removed")
        else:
            print(file_path + " Does not exist.")