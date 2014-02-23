#!/bin/bash
ps -A|grep angry|awk '{print $1}'|xargs kill -9
gdb -q ./angry*