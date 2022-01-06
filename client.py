from vidstream import ScreenShareClient
import socket
import pyautogui as pg
import pickle as pickle

pg.PAUSE = 0  # Pause between the moveTo function
server_IP = input("Enter the server IP address: ")


class Client:
    def __init__(self):
        self.streaming = False

    def streaming_function(self):
        """Starts/stops the streaming and the mouse tracking"""
        if self.streaming:
            print("[START STREAMING]....")
            self.client = ScreenShareClient(server_IP, 5050, x_res=1920, y_res=1080)
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect((server_IP, 1234))
            self.client.start_stream()
            self.receive_message()
        else:
            print("[STOP STREAMING]....")
            self.client.stop_stream()
            self.conn.close()

    def config_system(self):
        """When clicked the flag is changed to start/stop streaming"""
        self.streaming = not self.streaming
        self.streaming_function()

    def receive_message(self):
        """Receive message and moves/click"""
        while self.streaming:
            data = pickle.loads(self.conn.recv(4096))
            if isinstance(data, pg.Point):
                self.move_mouse_location(data)
            elif data == "LBP":
                self.mouse_click()

            print(data)

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
    pass


main()
