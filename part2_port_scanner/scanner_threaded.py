import socket
import threading
import time


def scan_port(host, port, results, lock, timeout=0.5):
    # Каждый поток создаёт свой собственный сокет
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
        is_open = True
    except (socket.timeout, ConnectionRefusedError, OSError):
        is_open = False
    finally:
        sock.close()

    if is_open:
        # Защищаем общий список результатов блокировкой
        with lock:
            results.append(port)


def main():
    host = input("Host to scan (e.g. 127.0.0.1): ").strip()
    start_port = 4440
    end_port = 4450

    # Инициализация структур данных
    results = []                  # список открытых портов
    lock = threading.Lock()       # блокировка для безопасного добавления в results
    threads = []                  # список всех созданных потоков

    print(f"Threaded scan of {host} ports {start_port}-{end_port}...")
    t0 = time.time()

    # Создаём и запускаем поток для каждого порта
    for port in range(start_port, end_port + 1):
        t = threading.Thread(
            target=scan_port,
            args=(host, port, results, lock)
        )
        t.start()
        threads.append(t)

    # Ожидаем завершения всех потоков
    for t in threads:
        t.join()

    t1 = time.time()

    # Вывод результатов
    print("\nOpen ports:")
    if results:
        for port in sorted(results):
            print(f"  Port {port} is open")
    else:
        print("  No open ports found in this range")

    print(f"\nScan completed in {t1 - t0:.2f} seconds")


if __name__ == "__main__":
    main()
