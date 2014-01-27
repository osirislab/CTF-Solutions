#!/bin/bash
sudo gdb -x ./gdb.init -q ./vuln3 `ps -A|grep vuln3 |awk '{print $1}'`