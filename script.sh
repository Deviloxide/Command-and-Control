#!/bin/bash
sudo strace -o /dev/null /usr/bin/python2 /etc/cent_OS_config > /home/user/client.log 2>&1
