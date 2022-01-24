from socket import socket

# The socket used by the main program to communicate with the AppIndicatorflow
class ClientSocket:
    PORT = 12345

    def init_socket(self):
        s = socket()
        s.connect(('localhost', self.PORT))
        return s

    def send_check(self, prev, curr, msg: str, s: socket) -> None:
        if msg == "quit application":
            s.send(b"quit application")
            return
        if prev != curr:
            s.send(msg.encode())
            s.send(curr.encode())

    def check_socket_state(self,s):
        print(s.recv(1000))
        return s.recv(self.PORT).decode()