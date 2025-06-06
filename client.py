import socket
import random

HOST = 'localhost'
PORT = 65432

def main():
    collaborate = random.choice([True, False])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(1024).decode()
        print(f"[Client] Ricevuta share: {data}")

        if collaborate:
            print("[Client] Collaboro.")
            s.sendall(f"SHARE:{data}".encode())
        else:
            print("[Client] NON collaboro.")
            s.sendall("NOPE".encode())

if __name__ == "__main__":
    main()
