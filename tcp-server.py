import socket

HOST = "127.0.0.1"
PORT = 5000

products = {}


def handle_command(command):
    global products

    command = command.strip()
    if not command:
        return "ERROR empty command"

    parts = command.split()
    cmd = parts[0].upper()

    if cmd == "ADD":
        if len(parts) < 3:
            return "ERROR usage: ADD key value"
        key = parts[1]
        value = " ".join(parts[2:])
        products[key] = value
        return "OK record add"

    elif cmd == "GET":
        if len(parts) != 2:
            return "ERROR usage: GET key"
        key = parts[1]
        if key not in products:
            return "ERROR invalid key"
        return f"DATA {products[key]}"

    elif cmd == "REMOVE":
        if len(parts) != 2:
            return "ERROR usage: REMOVE key"
        key = parts[1]
        if key not in products:
            return "ERROR invalid key"
        products.pop(key)
        return "OK value deleted"

    elif cmd == "LIST":
        if not products:
            return "DATA"
        items = ",".join(f"{k}={v}" for k, v in products.items())
        return f"DATA {items}"

    elif cmd == "COUNT":
        return f"DATA {len(products)}"

    elif cmd == "CLEAR":
        products.clear()
        return "OK all data deleted"

    elif cmd == "UPDATE":
        if len(parts) < 3:
            return "ERROR usage: UPDATE key new_value"
        key = parts[1]
        if key not in products:
            return "ERROR invalid key"
        new_value = " ".join(parts[2:])
        products[key] = new_value
        return "OK data updated"

    elif cmd == "POP":
        if len(parts) != 2:
            return "ERROR usage: POP key"
        key = parts[1]
        if key not in products:
            return "ERROR invalid key"
        value = products.pop(key)
        return f"DATA {value}"

    elif cmd == "QUIT":
        return "BYE"

    else:
        return "ERROR unknown command"


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"Server pornit pe {HOST}:{PORT}...")

    conn, addr = server_socket.accept()
    print(f"Client conectat de la {addr}")

    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            command = data.decode().strip()
            print(f"Comanda primita: {command}")

            response = handle_command(command)
            conn.sendall((response + "\n").encode())

            if command.upper() == "QUIT":
                break

    server_socket.close()
    print("Server oprit.")


if __name__ == "__main__":
    main()
