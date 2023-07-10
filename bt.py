import bluetooth

bluetooth.discover_devices()
addr = "2B:80:3C:F5:B5:A2"
port = 2

sock = bluetooth.BluetoothSocket()
sock.connect((addr, port))

while True:
    data = sock.recv(1024)
    if not data:
        break
    print(data)
