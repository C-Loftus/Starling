from socket import socket

# The socket used by the main program to communicate with the AppIndicatorflow
class ClientSocket:
    PORT = 12345
    s: socket = None

    def __init__(self) -> None:
        s = socket()
        s.connect(('localhost', self.PORT))
        self.s = s

    def check_to_send(self, prev, curr, msg: str) -> None:
        import os
        pid = os.getpid()

        if msg == "quit application":
            self.s.send((str(pid) + " quit application").encode())
            self.end_socket()
            return
        if prev != curr:
            print("sending \'" + msg + "\'")
            self.s.send(msg.encode())
    
    def end_socket(self):
        if self.s is not None:
            self.s.close()
            self.s = None
        
        

