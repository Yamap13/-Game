import socket
import time

wait_time = 0.5

IPADDR = "127.0.0.1"
PORT = 49152


sock_sv = socket.socket(socket.AF_INET)
sock_sv.bind((IPADDR, PORT))
sock_sv.listen()

# クライアントのリスト
client_list = []

# ○×シート
sheets = ['0','0','0','0','0','0','0','0','0']
message = []

def sum_check(sheets,num1,num2,num3):
     return abs(int(sheets[int(num1)])+int(sheets[int(num2)])+int(sheets[int(num3)])) == 3
def check(sheets):
    if sheets[4] != 0:
        if sum_check(sheets,0,4,8) or sum_check(sheets,1,4,7) or sum_check(sheets,2,4,6) or sum_check(sheets,3,4,5):
             return 1
    if sheets[0] != 0:
        if sum_check(sheets,0,1,2) or sum_check(sheets,0,3,6):
             return 1
    if sheets[8] != 0:
        if sum_check(sheets,2,5,8) or sum_check(sheets,6,7,8):
             return 1
    return 0
def main():          
    while len(client_list) < 2: #入室者管理
        sock_cl, addr = sock_sv.accept()
        # クライアントをリストに追加
        client_list.append((sock_cl, addr))
        client_list[len(client_list)-1][0].send("----------------------------".encode("utf-8"))
        time.sleep(wait_time)
        client_list[len(client_list)-1][0].send("           ○×Game           ".encode("utf-8"))
        time.sleep(wait_time)
        client_list[len(client_list)-1][0].send("----------------------------".encode("utf-8"))
        time.sleep(wait_time)
        client_list[len(client_list)-1][0].send("You entered the room".encode("utf-8"))
        time.sleep(wait_time)
        client_list[len(client_list)-1][0].send("Waiting for the opponent to enter the room".encode("utf-8"))
        time.sleep(wait_time)

    for client in client_list:
                client[0].send("Matching has been completed".encode("utf-8"))
    time.sleep(wait_time)

    client_list[0][0].send("You are first mover".encode("utf-8"))
    client_list[1][0].send("You are the latter".encode("utf-8"))
    time.sleep(wait_time)
    
    for client in client_list:
                    client[0].send("----------------------------".encode("utf-8"))
    time.sleep(wait_time)
    for client in client_list:
                client[0].send("          Game Start         ".encode("utf-8"))
    time.sleep(wait_time)

    coun = 0

    while coun < 9:
        while True:
            try:
                for client in client_list:
                    client[0].send("----------------------------".encode("utf-8"))
                time.sleep(wait_time)
                for client in client_list:
                    client[0].send(".".join(sheets).encode("utf-8"))
                time.sleep(wait_time)
                if coun % 2 == 0:
                    client_list[0][0].send("It is your turn".encode("utf-8"))
                    client_list[1][0].send("It is the opponent's turn".encode("utf-8"))
                    time.sleep(wait_time)
                else:   
                    client_list[0][0].send("It is the opponent's turn".encode("utf-8"))
                    client_list[1][0].send("It is your turn".encode("utf-8"))
                    time.sleep(wait_time)
                print(coun)
                print("受信待機")
                data = client_list[coun%2][0].recv(1024)
                num = int(data.decode("utf-8"))
                if data == b"":
                    break
                else:
                    if num < 10 :
                        if coun % 2 == 0:
                            sheets[num-1] = '1'
                        else:
                            sheets[num-1] = '-1'
                        coun += 1
                    if check(sheets): # 勝敗が決まった際の処理
                        for client in client_list:
                            client[0].send(".".join(sheets).encode("utf-8"))
                        time.sleep(wait_time)
                        for client in client_list:
                            client[0].send("----------------------------".encode("utf-8"))
                        time.sleep(wait_time)
                        if coun % 2 == 0:
                            client_list[0][0].send("You win".encode("utf-8"))
                            client_list[1][0].send("You lose".encode("utf-8"))
                        else:
                            client_list[1][0].send("You lose".encode("utf-8"))
                            client_list[0][0].send("You win".encode("utf-8"))
                        for client in client_list:
                            client[0].send("----------------------------".encode("utf-8"))
                        time.sleep(wait_time*4)
                        sock_cl.shutdown(socket.SHUT_RDWR)
                        sock_cl.close()
                    break
            except ConnectionResetError: # 接続エラー発生時の処理
                client_list.remove((sock_cl, addr)) # クライアントリストから削除

                for client in client_list:
                    client.send("Communication has been disconnected".encode("utf-8"))
                sock_cl.shutdown(socket.SHUT_RDWR)
                sock_cl.close()
    if not check(sheets):
        for client in client_list:
            client[0].send("----------------------------".encode("utf-8"))
        time.sleep(wait_time)
        for client in client_list:
            client[0].send("It was a draw".encode("utf-8"))
        time.sleep(wait_time)
        for client in client_list:
                client[0].send("----------------------------".encode("utf-8"))
        time.sleep(wait_time)
    sock_cl.shutdown(socket.SHUT_RDWR)
    sock_cl.close()
    
if __name__ == "__main__":
    main()
