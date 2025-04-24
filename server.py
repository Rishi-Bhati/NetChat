# Python program to implement server side of chat room.
import socket 
import select 
import sys 
from _thread import *
import traceback

"""
Socket Configuration:
- AF_INET: IPv4 addressing domain
- SOCK_STREAM: TCP socket for reliable, two-way, connection-based byte streams
"""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

# Check command line arguments
if len(sys.argv) != 3: 
	print("Correct usage: script, IP address, port number")
	exit() 

# Parse command line arguments
IP_address = str(sys.argv[1])  # IP address to bind to
Port = int(sys.argv[2])        # Port number to listen on

"""
Server Binding:
Binds the server to the specified IP address and port number.
The client must connect to this same IP and port.
"""
server.bind((IP_address, Port)) 

"""
Server Configuration:
Listen for up to 100 active connections simultaneously.
This number can be adjusted based on server capacity.
"""
server.listen(100) 

# List to keep track of all connected clients
list_of_clients = [] 

def clientthread(conn, addr): 
    """
    Function to handle individual client connections.
    Creates a separate thread for each client.
    
    Args:
        conn: Socket object for the client connection
        addr: Address information (IP, port) of the client
    """
    # Receive the username from the client
    try:
        username = conn.recv(2048).decode('utf-8')
    except Exception as e:
        print(f"Error receiving username from {addr[0]}: {str(e)}")
        username = addr[0]  # fallback to IP address if username not received

    # Send welcome message to newly connected client
    welcome_message = f"Welcome to this chatroom, {username}!"
    conn.send(welcome_message.encode('utf-8'))

    while True: 
        try: 
            # Receive message from client (up to 2048 bytes)
            message = conn.recv(2048)
            if message: 
                # Decode the received bytes to string
                decoded_message = message.decode('utf-8')
                
                # Print the message with sender's username
                print("<" + username + "> " + decoded_message)

                # Prepare message for broadcasting to all other clients
                message_to_send = "<" + username + "> " + decoded_message
                broadcast(message_to_send.encode('utf-8'), conn)
            else: 
                # Empty message indicates broken connection
                remove(conn)
                break

        except Exception as e:
            print(f"Error handling client {username}: {str(e)}")
            traceback.print_exc()
            continue

def broadcast(message, connection):
    """
    Broadcasts a message to all connected clients except the sender.
    
    Args:
        message: The message to broadcast (already encoded as bytes)
        connection: The sender's connection object to exclude from broadcast
    """
    for client in list_of_clients:
        if client != connection:
            try:
                client.send(message)
            except Exception as e:
                print(f"Error broadcasting to client: {str(e)}")
                client.close()
                # Remove the client if connection is broken
                remove(client)

def remove(connection):
    """
    Removes a client from the list of connected clients.
    
    Args:
        connection: The client connection to remove
    """
    if connection in list_of_clients:
        list_of_clients.remove(connection)
        print(f"Client removed from list. Active connections: {len(list_of_clients)}")

# Main server loop
try:
    while True:
        """
        Accept new client connections:
        - conn: Socket object for communication with the client
        - addr: Contains the IP address and port of the client
        """
        conn, addr = server.accept()
        
        # Add new client to the list for broadcasting
        list_of_clients.append(conn)
        
        # Log new connection with more details
        print(f"New connection from {addr[0]}:{addr[1]} - Total clients: {len(list_of_clients)}")
        
        # Create a new thread to handle this client
        start_new_thread(clientthread, (conn, addr))
        
except KeyboardInterrupt:
    print("\nServer shutting down...")
finally:
    # Clean up resources
    for client in list_of_clients:
        client.close()
    server.close()
    print("Server closed")
