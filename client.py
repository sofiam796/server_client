import numpy as np
import socket
import pickle

def generate_matrix():
    N, M, L = np.random.randint(1001, 2000, size=3)
    matrix1 = np.random.randint(0, 100, size=(N, M))
    matrix2 = np.random.randint(0, 100, size=(M, L))
    return matrix1, matrix2


def send_to_server(matrix1, matrix2, host="127.0.0.1", port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print("Підключення успішне.")

        data = {"matrix1": matrix1, "matrix2": matrix2}
        serialized_data = pickle.dumps(data)
        print(f"Підготовка до надсилання. Розмір даних: {len(serialized_data)} байт.")

        data_length = len(serialized_data)
        client_socket.sendall(data_length.to_bytes(8, 'big'))

        client_socket.sendall(serialized_data)
        print("Дані надіслано. Очікуємо відповідь.")

        response = b""
        while True:
            packet = client_socket.recv(4096)
            if not packet:
                break
            response += packet

        print("Відповідь отримано.")
        return pickle.loads(response)

if __name__ == "__main__":
    matrix1, matrix2 = generate_matrix()
    response = send_to_server(matrix1, matrix2)
