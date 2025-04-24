# Python program to implement client side of chat room.
import socket 
import select 
import sys 
import traceback

def setup_connection():
    """
    Sets up the socket connection to the server.
    
    Returns:
        socket: Connected socket object or None if connection fails
    """
    try:
        # Create TCP/IP socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow socket to reuse local addresses
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Check command line arguments
        if len(sys.argv) < 3 or len(sys.argv) > 4: 
            print("Correct usage: script, IP address, port number [local_port]")
            print("Example: python client.py 127.0.0.1 12345")
            print("Example with local port: python client.py 127.0.0.1 12345 50001")
            return None
            
        # Parse command line arguments
        IP_address = str(sys.argv[1])  # Server IP address
        Port = int(sys.argv[2])        # Server port number
        
        # If local port is specified, bind to it
        if len(sys.argv) == 4:
            local_port = int(sys.argv[3])
            try:
                server.bind(('', local_port))
                print(f"Bound to local port {local_port}")
            except OSError as e:
                print(f"Warning: Could not bind to local port {local_port}: {e}")
                print("Continuing with automatically assigned port...")
        
        # Connect to the server
        print(f"Connecting to server at {IP_address}:{Port}...")
        server.connect((IP_address, Port))
        print("Connected to the server")
        return server
    except Exception as e:
        print(f"Connection error: {str(e)}")
        traceback.print_exc()
        return None

# Establish connection to the server
server = setup_connection()
if not server:
    print("Failed to connect to the server. Exiting.")
    sys.exit(1)

try:
    print("Welcome to the chat room! Type your messages and press Enter to send.")
    print("Press Ctrl+C to exit.")
    name = input("Enter your name: ")
    server.send(name.encode('utf-8'))  # Send name to server
    print(f"Welcome {name}! You can start chatting now.")
    while True: 
        # List of input sources to monitor (terminal input and server messages)
        sockets_list = [sys.stdin, server] 

        """
        Select monitors multiple input channels:
        - stdin: For user typing messages
        - server: For receiving messages from other clients
        
        When data is available on any of these channels, select will return
        that channel in read_sockets.
        """
        read_sockets, write_socket, error_socket = select.select(sockets_list, [], []) 

        for sock in read_sockets: 
            # If message is from the server
            if sock == server: 
                try:
                    # Receive and decode message from server
                    message = sock.recv(2048)
                    name = sock.getpeername()  # Get the server's IP address and port
                    
                    # Empty message means server disconnected
                    if not message:
                        print("\nDisconnected from server")
                        sys.exit(0)
                        
                    # Print the received message
                    print(message.decode('utf-8'))
                except Exception as e:
                    print(f"\nError receiving message: {str(e)}")
                    sys.exit(1)
            # If user entered a message
            else: 
                # Read message from terminal
                message = sys.stdin.readline()
                
                # Send encoded message to server
                server.send(message.encode('utf-8'))
                
                # Display the message in the terminal
                sys.stdout.write("<You> ")
                sys.stdout.write(message)
                sys.stdout.flush() 

except KeyboardInterrupt:
    print("\nExiting chat room...")
except Exception as e:
    print(f"\nAn error occurred: {str(e)}")
    traceback.print_exc()
finally:
    # Clean up resources
    if server:
        server.close()
    print("Connection closed")
