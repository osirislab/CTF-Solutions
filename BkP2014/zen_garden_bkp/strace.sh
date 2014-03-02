#!/bin/bash

ulimit -c unlimited

socat TCP-LISTEN:2323,reuseaddr,fork EXEC:"strace -f ./zengarden-9b81162aea2ed4be3838faff59b3fd1b"

