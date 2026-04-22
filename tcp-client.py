import socket

HOST = "127.0.0.1"
PORT = 5000

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    print("Conectat la server.")
    print("Scrie comenzi: ADD, GET, REMOVE, LIST, COUNT, CLEAR, UPDATE, POP, QUIT")

    while True:
        command = input(">> ").strip()
        if not command:
            continue

        client_socket.sendall((command + "\n").encode())
        response = client_socket.recv(1024).decode().strip()
        print("Server:", response)

        if command.upper() == "QUIT":
            break

    client_socket.close()
    print("Client inchis.")


if __name__ == "__main__":
    main()
