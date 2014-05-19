#!/bin/bash
socat TCP-LISTEN:2323,reuseaddr,fork EXEC:"./sftp_bf28442aa4ab1a4089ddca16729b29ac"
