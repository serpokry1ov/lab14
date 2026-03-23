import socket
import time

def scan_port(host, port, timeout=0.5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
        return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False
    finally:
        sock.close()

def main():
    host = input("Host to scan (e.g. 127.0.0.1): ").strip()
    start_port = 4440
    end_port = 4450

    print("Sequential scan of {} ports {}-{}...".format(host, start_port, end_port))
    t0 = time.time()
    for port in range(start_port, end_port + 1):
        if scan_port(host, port):
            print("Port {} is OPEN".format(port))
    t1 = time.time()
    print("Sequential scan finished in {:.2f} seconds".format(t1 - t0))

if __name__ == "__main__":
    main()
