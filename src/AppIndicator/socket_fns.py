from socket import socket

# The socket used by the main program to communicate with the AppIndicatorflow
class ClientSocket:
    PORT = 9999
    s: socket = None

    def __init__(self) -> None:
        import os
        pid = os.getpid()
        s = socket()
        s.connect(('localhost', self.PORT))
        message=("pid:" + str(pid)).encode()
        s.send(message)

        self.s = s

    def check_to_send(self, prev, curr, msg) -> None:

        msg = ''.join(msg)
        print("Checking to send: ", msg)

        if msg == "quit application":
            self.s.send(("quit application").encode())
            self.end_socket()
            return
        if prev != curr:
            print("sending \'" + msg + "\'")
            self.s.send(msg.encode())
    
    def end_socket(self):
        if self.s is not None:
            self.s.close()
            self.s = None
        
        

