import time
import win32api
from vidstream import StreamingServer
import threading
import socket
import pyautogui as pg
import pickle as pickle


class Server:
    def __init__(self):
        self.server = StreamingServer('', 5050)
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.bind(('', 1234))
        self.conn.listen(5)
        self.client_socket, address = self.conn.accept()
        self.running = True

    def start_stream(self):
        """start the streaming of the other screen"""
        self.server.start_server()
        print(f"Connection from  has been established!")

    def click_mouse(self):
        """Tells when mouse is clicked and send to client to click as well"""
        state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
        state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128

        while self.running:
            get_state_left = win32api.GetKeyState(0x01)
            get_state_right = win32api.GetKeyState(0x02)
            state = ""
            if get_state_left != state_left:  # Button state changed
                state_left = get_state_left
                if get_state_left < 0:
                    state = 'LBP'  # Left button press
                else:
                    state = 'LBR'  # Left button release

            if get_state_right != state_right:  # Button state changed
                state_right = get_state_right
                if get_state_right < 0:
                    state = 'RBP'  # Right button press
                else:
                    state = 'RBR'  # Right button release
            if state:
                data = pickle.dumps(state)
                self.client_socket.send(data)
            time.sleep(0.001)

    def send_mouse_location(self):
        """start the streaming of the cursor data"""
        current_location = pg.Point(0, 0)

        while self.running:
            current_mouse_location = pg.position()
            if current_mouse_location != current_location:
                current_location = current_mouse_location
                data = pickle.dumps(current_mouse_location)
                self.client_socket.send(data)
            else:
                pass  # Do nothing if the cursor is at the same location


if __name__ == '__main__':
    server = Server()
    print("Server is up!")
    """Declaring and starting the threads"""
    t = threading.Thread(target=server.start_stream)
    t2 = threading.Thread(target=server.send_mouse_location)
    t3 = threading.Thread(target=server.click_mouse)

    t.start()
    t2.start()
    t3.start()



