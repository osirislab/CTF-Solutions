import requests

flag = [''] * 0x100

for i in range(0x100, 0x3986):
    j = requests.post("http://something.420blaze.in:8545/", data='{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["'+hex(i)+'", true],"id":1}', headers={"Content-Type": "application/json"}).json()
    for tx in j['result']['transactions']:
        func = tx['input'][2:10]
        arg1 = tx['input'][10:10+64]
        arg2 = tx['input'][74:74+64]
        arg3 = tx['input'][74+64:202]
        arg4 = tx['input'][202:].decode('hex').rstrip('\x00')
        if func == 'd1d13ebf':
            idx = int(arg1[-2:], 16)
            char = arg4[-1]
            flag[idx] = char
            print(flag)

