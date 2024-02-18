import select
import threading
import socket
import paramiko
import os
from paramiko import SSHClient

# SSH server configuration
ssh_host = os.getenv('SSH_HOST')
ssh_port = int(os.getenv('SSH_PORT'))
ssh_password = os.getenv('SSH_PASSWORD')

# Port forwarding configuration
local_port = int(os.getenv('LOCAL_PORT'))
remote_host = os.getenv('REMOTE_HOST')
remote_port = int(os.getenv('REMOTE_PORT'))

# Enable verbose logging (mimics -v)
paramiko.util.log_to_file("ssh.log")

def reverse_forward_tunnel(local_port, remote_host, remote_port, transport):
    transport.request_port_forward(address=remote_host, port=remote_port)
    while True:
        chan = transport.accept(1000)
        if chan is None:
            continue
        thr = threading.Thread(target=handler, args=(chan, local_port))
        thr.setDaemon(True)
        thr.start()

def handler(chan, port):
    sock = socket.socket()
    try:
        sock.connect(('localhost', port))
    except Exception as e:
        print(f'Forwarding request to localhost:{port} failed: {e}')
        return
    
    while True:
        r, w, x = select.select([sock, chan], [], [])
        if sock in r:
            data = sock.recv(1024)
            if len(data) == 0:
                break
            chan.send(data)
        if chan in r:
            data = chan.recv(1024)
            if len(data) == 0:
                break
            sock.send(data)

    chan.close()
    sock.close()

def forward_port():
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print("Connecting to SSH server")
    client.connect(hostname=ssh_host, port=ssh_port, password=ssh_password)
    
    print("Setting up remote port forwarding")
    reverse_forward_tunnel(local_port, remote_host, remote_port, client.get_transport())

    client.close()

if __name__ == '__main__':
    forward_port()
