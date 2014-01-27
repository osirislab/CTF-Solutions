#!/bin/bash

ps -A|egrep "bug$"|awk '{print $1}'| sudo xargs kill -9
sudo gdb -q -x gdb.init ./bug 