#!/bin/bash

##### Simulation parameters
N=5              
T=2              
PASSWORD="ciao123"
#####

# Start the server in background
echo "[*] Starting the server..."
python3 server.py $N $T "$PASSWORD" > server_output.log &
SERVER_PID=$!

# Wait for the server to start
sleep 1

# Start the clients and wait for them to finish
echo "[*] Starting $N ... clients"
for ((i=1; i<=N; i++)); do
    python3 client.py > client_output_$i.log &
done
wait

echo
echo "===== SERVER ====="
cat server_output.log
echo
for ((i=1; i<=N; i++)); do
    echo "===== CLIENT $i ====="
    cat client_output_$i.log
    echo
done

# Terminate the server process if still active, ignoring errors (e.g.)
# server already terminated.
kill $SERVER_PID 2>/dev/null
