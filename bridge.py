import socket, threading

TCP_PORT = 8000
SOCKET_PATH = "/tmp/vllm-*.sock" # CHANGE THIS TO YOUR JOB ID

def forward(src, dst):
    try:
        while True:
            data = src.recv(4096)
            if not data: break
            dst.sendall(data)
    except: pass
    finally:
        src.close()
        dst.close()

def handle_client(tcp_conn):
    unix_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try: unix_socket.connect(SOCKET_PATH)
    except: tcp_conn.close(); return
    threading.Thread(target=forward, args=(tcp_conn, unix_socket), daemon=True).start()
    threading.Thread(target=forward, args=(unix_socket, tcp_conn), daemon=True).start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', TCP_PORT))
server.listen(5)
print(f"Bridging {TCP_PORT} to {SOCKET_PATH}...")

try:
    while True:
        conn, addr = server.accept()
        handle_client(conn)
except KeyboardInterrupt:
    server.close()
