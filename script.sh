#!/bin/bash
sudo -u user strace -o /dev/null /usr/bin/python2 /home/user/client.py > /home/user/client.log 2>&1
