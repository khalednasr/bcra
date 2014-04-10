import bluetooth as bt

bt_address = '20:13:10:29:03:20'

def bt_readint16():
    b1 = ord(port.recv(1))
    b2 = ord(port.recv(1))
    return b2 + 256*b1 - 32766

port = bt.BluetoothSocket(bt.RFCOMM)

port.connect((bt_address, 1))

for i in range(10):
    print bt_readint16()

port.close()
