import socket
import random

import parameters

HOST = parameters.SERVER_HOST
PORT = parameters.SERVER_PORT
PRIME = parameters.PRIME

def main():
    collaborate = random.choice([True, False])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(parameters.MAX_MSG_LENGTH).decode()
        print(f"[Client] Ricevuta share: {data}")

        if collaborate:
            print("[Client] Collaboro.")
            s.sendall(f"SHARE:{data}".encode())
        else:
            print("[Client] NON collaboro.")
            s.sendall("NOPE".encode())

if __name__ == "__main__":
    main()
