#!/bin/bash
socat TCP-LISTEN:2323,reuseaddr,fork EXEC:"./chall_heap"
