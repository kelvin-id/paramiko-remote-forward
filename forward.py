from select import select
from threading import Thread
from socket import socket
from os import getenv
from paramiko import SSHClient, AutoAddPolicy, util
# from dotenv import load_dotenv, find_dotenv

# env_file = find_dotenv(".env")
# load_dotenv(env_file)

# SSH server configuration
ssh_host = getenv('SSH_HOST')
ssh_port = int(getenv('SSH_PORT'))
ssh_password = getenv('SSH_PASSWORD')

# Port forwarding configuration
local_port = int(getenv('LOCAL_PORT'))
remote_host = getenv('REMOTE_HOST')
remote_port = int(getenv('REMOTE_PORT'))

# Enable verbose logging (mimics -v)
util.log_to_file("ssh.log")

def reverse_forward_tunnel(local_port, remote_host, remote_port, transport):
    transport.request_port_forward(address=remote_host, port=remote_port)
    while True:
        chan = transport.accept(1000)
        if chan is None:
            continue
        thr = Thread(target=handler, args=(chan, local_port))
        thr.setDaemon(True)
        thr.start()

def handler(chan, port):
    sock = socket()
    try:
        sock.connect(('localhost', port))
    except Exception as e:
        print(f'Forwarding request to localhost:{port} failed: {e}')
        return
    
    while True:
        r, w, x = select([sock, chan], [], [])
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
    client.set_missing_host_key_policy(AutoAddPolicy())
    
    print("Connecting to SSH server")
    client.connect(hostname=ssh_host, port=ssh_port, password=ssh_password)
    
    print("Setting up remote port forwarding")
    reverse_forward_tunnel(local_port, remote_host, remote_port, client.get_transport())

    client.close()

if __name__ == '__main__':
    forward_port()
