import socket
import threading

# Note: first player is the player send his nickname for first

# Lists for clients and their nicknames
clients = []
first_player = None
second_player = None

# Handling messages to all connected clients
def handle_client(client):
    
    try:
        while True:
            # Broadcasting messages
            msg = client.recv(1024)
            for c in clients:
                if c == client:
                    continue
                print(msg)
                c.send(msg)

    except Exception as e:
        # Removing and closing clients
        idx = clients.index(client)
        clients.remove(client)
        print(f"[!] Errore durante la gestione del client {client.getpeername()[0]}: {str(e)}")

    finally:
        client.close()
        print(f"[!] Connessione con il client chiusa")


# Receiving / Listening function
def receive():
    
    global first_player
    global second_player

    while True:
        # Accept connection
        client, address = server.accept()
        print("[+] Connected with {}".format(str(address)))

        # Request and store nickname
        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        if first_player is None:
            first_player = client
            print("[!] First player: " + nickname)
            client.send('FIRST'.encode('ascii'))
        else:
            second_player = client
            print("[!] Second player: " + nickname)
            client.send('SECOND'.encode('ascii'))
        clients.append(client)        

        # Starts handling thread for client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()



if __name__ == '__main__':

    # Server connection data
    HOST = '0.0.0.0'
    PORT = 55555

    # Starting server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("[!] Server in ascolto sulla porta " + str(PORT) + "...")

    receive()
