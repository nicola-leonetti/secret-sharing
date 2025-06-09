import socket
import threading
import sys
import random

import parameters

HOST = parameters.SERVER_HOST
PORT = parameters.SERVER_PORT
PRIME = parameters.PRIME

class Server:
    def __init__(self, n, t, password):
        self.n = n
        self.t = t
        self.password = password
        self.shares = self.generate_shares(password, t, n)
        self.received = []
        self.lock = threading.Lock()

    def str_to_int(self, s):
        return int.from_bytes(s.encode(), 'big')

    def int_to_str(self, n):
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

    def eval_poly(self, coeffs, x):
        result = 0
        for i, coef in enumerate(coeffs):
            result = (result + coef * pow(x, i, PRIME)) % PRIME
        return result

    def generate_shares(self, secret, t, n):
        s = self.str_to_int(secret)
        coeffs = [s] + [random.randrange(0, PRIME) for _ in range(t - 1)]
        return [(i, self.eval_poly(coeffs, i)) for i in range(1, n + 1)]

    def lagrange_interpolate(self, x, x_s, y_s):
        """
        Given a list of x-values and y-values, calculate the value of 
        the Lagrange polynomial at x by performing Lagrange 
        interpolation.
        """
        total = 0
        # Build the i-th Lagrange term for each couple and sum each of 
        # the terms mod PRIME
        # The i-th term is given by the product of (x - xj)/(xi - xj) 
        # for each j != i.
        for i in range(len(x_s)):
            xi, yi = x_s[i], y_s[i]
            prod = yi
            for j in range(len(x_s)):
                if i != j:
                    xj = x_s[j]
                    inv = pow(xi - xj, -1, PRIME)
                    prod *= (x - xj) * inv
                    prod %= PRIME
            total += prod
            total %= PRIME
        return total

    def handle_client(self, conn, addr, idx):
        """
        Handler for the idx-th client. The handler is run in parallel
        for each connection to the server.
        """
        # Send share to the client
        conn.sendall(f"{self.shares[idx][0]},{self.shares[idx][1]}".encode())

        # Receive and parse data from the idx-th client
        data = conn.recv(parameters.MAX_MSG_LENGTH).decode()
        if data.startswith("SHARE:"):
            x_str, y_str = data[len("SHARE:"):].split(",")
            with self.lock:
                self.received.append((int(x_str), int(y_str)))
                print(f"[+] Ricevuta share da {addr}")
        else:
            print(f"[-] Client {addr} non ha collaborato.")
        conn.close()

    def run(self):
        print("[*] Password distribuita. Ora viene cancellata dalla memoria.")
        self.password = None

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen()
            print(f"[*] In ascolto su {HOST}:{PORT}")

            threads = []
            for i in range(self.n):
                conn, addr = s.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr, i))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

        if len(self.received) >= self.t:
            x_s, y_s = zip(*self.received[:self.t])
            # Interpolate coefficients to get the total secret.
            secret_int = self.lagrange_interpolate(0, x_s, y_s)
            try:
                password = self.int_to_str(secret_int)
                print(f"[+] Password ricostruita: {password}")
            except UnicodeDecodeError:
                print("[-] Errore nella decodifica della password.")
        else:
            print("[-] Ricostruzione fallita: non abbastanza share.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python server.py <n> <t> <password>")
        sys.exit(1)

    n = int(sys.argv[1])
    t = int(sys.argv[2])
    password = sys.argv[3]

    server = Server(n, t, password)
    server.run()
