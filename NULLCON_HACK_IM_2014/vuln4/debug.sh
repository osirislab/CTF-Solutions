#!/bin/bash
sudo gdb -x ./gdb.init -q ./chall_heap `ps -A|grep chall_heap |awk '{print $1}'`