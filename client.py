import time
from vidstream import ScreenShareClient
import socket
import threading
import pyautogui as pg
import pickle as pickle

running = True
pg.PAUSE = 0  # Pause between the moveTo function
server_IP = input("Enter the server IP address: ")


class Streaming:
    def __init__(self):
        """Initialize the connections with the server"""
        self.client = ScreenShareClient(server_IP, 5050, x_res=1920, y_res=1080)
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def streaming_function(self):
        """Shares the screen with the server"""
        print("[START STREAMING]....")
        self.client.start_stream()
        while running:
            time.sleep(1)

        print("[STOP STREAMING]....")
        self.client.stop_stream()


class Messages:
    def __init__(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive_message(self):
        """Receive message and moves/click"""
        self.conn.connect((server_IP, 1234))
        while True:
            data = pickle.loads(self.conn.recv(4096))
            if isinstance(data, pg.Point):
                MouseControl.move_mouse_location(data)
            elif data == "LBP":
                MouseControl.mouse_click()

            print(data)


class MouseControl:
    @staticmethod
    def move_mouse_location(location):
        """Moving the mouse location to X, Y coordinates"""
        try:
            pg.moveTo(location.x, location.y, )

        except KeyboardInterrupt:
            print("There's an error..")

    @staticmethod
    def mouse_click():
        """Clicking the mouse"""
        try:
            pg.click()
        except KeyboardInterrupt:
            print("There's an error..")


def main():
    streaming = Streaming()
    receive = Messages()
    t = threading.Thread(target=streaming.streaming_function)
    t2 = threading.Thread(target=receive.receive_message)

    t.start()
    t2.start()


main()
