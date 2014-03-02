# Level 1: make failed connections to the ports defined in the program
nc -v 54.186.19.76 4511; nc -v 54.186.19.76 4527; nc -v 54.186.19.76 4539; nc -v 54.186.19.76 4552; nc -v 54.186.19.76 4538
# Level 2: send it 0xdeadb00b ^ 0x12F9BC11
python -c "print '\xcc\x54\x0c\x1a'[::-1]" | nc -u 54.186.19.76 4777
# Leve 3: send it 11 zeroes to satisfy the bunch of xors at the end
python -c "print '\x00'*44"| nc -u 54.186.19.76 4777
# final connection
nc 54.186.19.76 9999
