import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 4444))

response = client.recv(1024).decode()
print(response)
account_name = input()
client.sendall(account_name.encode())

response = client.recv(1024).decode()
print(response)
pin = input()
client.sendall(pin.encode())

while True:
    response = client.recv(1024).decode()
    print(response)
    choice = input()
    client.sendall(choice.encode())
    
    if choice == "4":
        break
    
    if choice in ["2", "3"]:
        amount = input("Enter amount: ")
        client.sendall(amount.encode())
    
    operation_result = client.recv(1024).decode()
    print(operation_result)

client.close()
