from vidstream import ScreenShareClient
import socket
import pyautogui as pg
import pickle as pickle
import threading

pg.PAUSE = 0  # Pause between the moveTo function


class Client:
    def __init__(self):
        self.sharing = False

    def streaming_function(self, server_IP):
        """Takes the IP and starting the streaming and the mouse tracking"""
        if self.sharing:
            print("[START STREAMING]....")
            self.client = ScreenShareClient(server_IP, 5050, x_res=1920, y_res=1080)
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect((server_IP, 1234))
            self.client.start_stream()
            t = threading.Thread(target=self.receive_message)
            t.start()
        else:
            self.client.stop_stream()
            self.conn.close()
            print("\n[CONNECTION CLOSED]....")

    def start_server(self, server_IP):
        """Takes the Server IP and enabling the server"""
        if not self.sharing:
            self.sharing = True
            self.streaming_function(server_IP)

    def stop_server(self, server_IP):
        """Takes the Server IP and stops the server"""
        if self.sharing:
            self.sharing = False
            self.streaming_function(server_IP)

    def receive_message(self):
        """Receive message and moves/click"""
        while self.sharing:
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
            pg.moveTo(location.x, location.y)

        except KeyboardInterrupt as e:
            raise Exception(e)

    @staticmethod
    def mouse_click():
        """Clicking the mouse"""
        try:
            pg.click()
        except KeyboardInterrupt as e:
            raise Exception(e)
