# Python program to implement client side of chat room.
import socket 
import select 
import sys 
import traceback
import threading
import platform

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

def input_thread_func(server_socket, stop_event):
    try:
        while not stop_event.is_set():
            message = sys.stdin.readline()
            if not message:
                break
            server_socket.send(message.encode('utf-8'))
            sys.stdout.write("<You> ")
            sys.stdout.write(message)
            sys.stdout.flush()
    except Exception as e:
        print(f"\nError sending message: {str(e)}")
        stop_event.set()

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

    stop_event = threading.Event()
    is_windows = platform.system() == "Windows"

    if is_windows:
        # On Windows, use a thread to read user input
        input_thread = threading.Thread(target=input_thread_func, args=(server, stop_event), daemon=True)
        input_thread.start()

        while not stop_event.is_set():
            read_sockets, _, _ = select.select([server], [], [], 0.5)
            for sock in read_sockets:
                if sock == server:
                    try:
                        message = sock.recv(2048)
                        if not message:
                            print("\nDisconnected from server")
                            stop_event.set()
                            break
                        print(message.decode('utf-8'))
                    except Exception as e:
                        print(f"\nError receiving message: {str(e)}")
                        stop_event.set()
                        break
        input_thread.join()
    else:
        # On non-Windows, use select on stdin and server socket
        while True:
            sockets_list = [sys.stdin, server]
            read_sockets, _, _ = select.select(sockets_list, [], [])
            for sock in read_sockets:
                if sock == server:
                    try:
                        message = sock.recv(2048)
                        if not message:
                            print("\nDisconnected from server")
                            sys.exit(0)
                        print(message.decode('utf-8'))
                    except Exception as e:
                        print(f"\nError receiving message: {str(e)}")
                        sys.exit(1)
                else:
                    message = sys.stdin.readline()
                    server.send(message.encode('utf-8'))
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
