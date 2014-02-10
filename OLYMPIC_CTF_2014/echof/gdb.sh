#!/bin/bash

sudo gdb ./a.out `ps -A|egrep "task$"|awk '{print $1}'`