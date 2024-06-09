import socket, threading

accounts = {
    "Sedra": 1000,
    "Rasha": 1500
}

def handle_client(client_socket, client_address):
    print("Accepted connection from {}".format(client_address))
    
    client_socket.sendall(b"Welcome to the Bank ATM. Please enter your account name: ")
    account_name = client_socket.recv(1024).decode().strip()
    
    if account_name not in accounts:
        client_socket.sendall(b"Account not found. Connection closed.")
        client_socket.close()
        return
    
    client_socket.sendall("Hello, {}. Please enter your PIN: ".format(account_name).encode())
    pin = client_socket.recv(1024).decode().strip()
    
    while True:
        client_socket.sendall(b"Available operations:\n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Exit\nEnter your choice: ")
        choice = client_socket.recv(1024).decode().strip()
        
        if choice == "1":
            client_socket.sendall("Your current balance is: {}".format(accounts[account_name]).encode())
        elif choice == "2":
            amount = float(client_socket.recv(1024).decode().strip())
            accounts[account_name] += amount
            client_socket.sendall("Deposit successful. Your updated balance is: {}".format(accounts[account_name]).encode())
        elif choice == "3":
            amount = float(client_socket.recv(1024).decode().strip())
            if amount > accounts[account_name]:
                client_socket.sendall(b"Insufficient funds.")
            else:
                accounts[account_name] -= amount
                client_socket.sendall("Withdrawal successful. Your updated balance is: {}".format(accounts[account_name]).encode())
        elif choice == "4":
            break
    
    print("Closing connection with {}".format(client_address))
    client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 4444))
server.listen(5)
print("Server listening on port 0.0.0.0")

while True:
    client_socket, client_address = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
