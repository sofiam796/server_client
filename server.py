import numpy as np
import socket
from concurrent.futures import ThreadPoolExecutor
import pickle

def multiply_matrix(matrix1, matrix2):
    return np.dot(matrix1, matrix2)

def client_session(client_socket):
    try:
        data_length = int.from_bytes(client_socket.recv(8), 'big')
        print(f"Очікуємо {data_length} байт даних.")
        data = b""
        while len(data) < data_length:
            packet = client_socket.recv(4096)
            if not packet:
                break
            data += packet
        print("Дані отримано.")

        data_matrix = pickle.loads(data)
        matrix1 = data_matrix["matrix1"]
        matrix2 = data_matrix["matrix2"]
        print(f"Розмір першої матриці: {matrix1.shape}, другої матриці: {matrix2.shape}")

        if matrix1.shape[1] != matrix2.shape[0]:
            error_message = "Розміри матриць не підходять під множення."
            client_socket.sendall(pickle.dumps({"error": error_message}))
            print(error_message)
            return
        
        print("Множення матриць.")
        result = multiply_matrix(matrix1, matrix2)
        print("Множення завершено. Надсилаємо результат.")
        client_socket.sendall(pickle.dumps(result))

    except Exception as e:
        print(f"error: {e}")
        client_socket.sendall(pickle.dumps({"error": str(e)}))
    finally:
        client_socket.close()


def start_server(host="127.0.0.1", port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Сервер запущено.")

        with ThreadPoolExecutor() as executor:
            while True:
                client_socket, addr = server_socket.accept()
                print(f"Нове підключення: {addr}")
                executor.submit(client_session, client_socket)


if __name__ == "__main__":
    start_server()