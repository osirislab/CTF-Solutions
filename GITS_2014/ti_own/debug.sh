#!/bin/bash
ps -A|egrep " ti$"|awk '{print $1}'|sudo xargs kill -9
sudo gdb -x ./gdb.init -q ./ti
