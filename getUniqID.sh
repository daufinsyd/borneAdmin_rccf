#!/usr/bin/bash
# 12/01/17 on sydney_manjaro@sydney-manjaro

# Return an unique and unchangeable ID

/sbin/blkid | grep "$(df -h / | sed -n 2p | cut -d" " -f1):" | grep -o "UUID=\"[^\"]*\" " | sed "s/UUID=\"//;s/\"//"''''
