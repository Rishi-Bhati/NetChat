# Python Chat Application - Client/Server System

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Starting the Server](#starting-the-server)
  - [Connecting Clients](#connecting-clients)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Security Considerations](#security-considerations)
- [License](#license)

## Project Overview
A Python-based chat application demonstrating client-server architecture using TCP sockets. Supports multiple concurrent clients with message broadcasting.

## Features
- Multi-client chat room
- Username identification
- Message broadcasting
- Graceful connection handling
- Cross-platform compatibility
- Optional client port binding

## Requirements
- Python 3.6+
- Any modern operating system (Windows/Linux/macOS)
- Network access between client and server

## Installation
```bash
# Clone the repository (if applicable)
git clone https://example.com/chat-app.git
cd chat-app

# No additional dependencies required
```

## Usage

### Starting the Server
```bash
python server.py <IP_ADDRESS> <PORT>
# Example (localhost on port 12345):
python server.py 127.0.0.1 12345
```

### Connecting Clients
```bash
# Basic connection:
python client.py <SERVER_IP> <SERVER_PORT>

# With optional local port binding:
python client.py <SERVER_IP> <SERVER_PORT> <LOCAL_PORT>

# Example connection:
python client.py 127.0.0.1 12345
```

## Configuration
| Component | Arguments | Description |
|-----------|-----------|-------------|
| Server    | IP_ADDRESS PORT | Bind server to specified interface and port |
| Client    | SERVER_IP SERVER_PORT [LOCAL_PORT] | Connect to server with optional local port binding |

## Troubleshooting
### Common Issues
1. **"Address already in use" error**
   - Wait 1-2 minutes for OS to release the port
   - Use different port number

2. **Connection refused errors**
   - Verify server is running
   - Check firewall settings
   - Ensure matching IP/port between client and server

3. **Message display issues**
   - Ensure UTF-8 encoding
   - Check network stability

4. **WinError 10038 on Windows when running client**
   - This error occurs because Windows does not support using `select.select` on `sys.stdin`.
   - The client has been updated to use a separate input thread on Windows to read user input asynchronously.
   - To avoid this error, ensure you are using the latest client.py version with this fix.
   - On non-Windows platforms, the original select-based input handling is retained.



## Security Considerations
⚠️ **Important:** This is a demonstration application. Not recommended for production use.

- No encryption (messages sent in plain text)
- No authentication beyond username
- No message persistence
- Open to port scanning

For secure implementations:
- Use SSH tunneling
- Implement TLS encryption
- Add user authentication

## License
This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
