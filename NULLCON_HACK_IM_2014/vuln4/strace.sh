#!/bin/bash
socat TCP-LISTEN:2323,reuseaddr,fork EXEC:"strace -f ./chall_heap"
