import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Определение целевого IP
target = input("Введите IP адрес целевого хоста: ")
# Определение диапазона портов для сканирования
start_port = int(input("Введите начальный порт: "))
end_port = int(input("Введите конечный порт: "))
# Получение IP адреса
target_ip = socket.gethostbyname(target)
# Выводим информацию о сканировании
print(f"Начало сканирования {target_ip}")
print(f"Диапазон портов: {start_port} - {end_port}")
print(f"Время начала: {datetime.now()}")
print("-" * 50)

# Функция для сканирования порта
def scan_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((target_ip, port))
    sock.close()
    return port, result == 0

# Сканирование портов с многопоточностью
with ThreadPoolExecutor(max_workers=100) as executor:
    futures = [executor.submit(scan_port, port) for port in range(start_port, end_port + 1)]
    for future in futures:
        port, is_open = future.result()
        if is_open:
            print(f"Порт {port} открыт")
        else:
            print(f"Порт {port} закрыт")
            print(f"Время окончания: {datetime.now()}")
