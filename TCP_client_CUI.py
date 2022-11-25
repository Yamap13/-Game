import socket

wait_time = 3
sheets = []

def print_sheets(sheets):
    coun = 0
    print("---------------")
    for k in range(3):
        for l in range(3):
            if int(sheets[coun]) == 1:
                print("| ○ |",end = '')
            elif int(sheets[coun]) == -1:
                print("| × |",end = '')
            else:
                print("| {} |".format(str(coun+1)),end = '')
            coun += 1
        print('')
        print("---------------")
    print('')

IPADDR = "127.0.0.1"
PORT = 49152

sock = socket.socket(socket.AF_INET)
sock.connect((IPADDR, PORT))

while True:
    try:
        data = sock.recv(1024)
        
        if data == b"":
            break
        elif data == b"It is your turn":
            print(data.decode("utf-8")+"\n")
            while True:
                try:
                    data = input("Please enter numbers 1~9 > ")
                    print('')
                    if 0<int(data)<10 and int(sheets[int(data)-1]) == 0:
                        sock.send(data.encode("utf-8"))
                        break
                    else:
                        print("Incorrect input.\n")
                except ConnectionResetError:
                    sock.shutdown(socket.SHUT_RDWR)
                    sock.close()
        elif '.' in data.decode("utf-8"):
            sheets = data.decode("utf-8").split('.')
            print_sheets(sheets)
        else:
            print(data.decode("utf-8")+"\n")
        
    except ConnectionResetError:
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()    
        break
