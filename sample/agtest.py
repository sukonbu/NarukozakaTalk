# -*- coding: utf-8 -*-
import socket
import string
import os
import subprocess
import time

host = 'localhost'  # localhost
port = 10500   # juliusサーバーモードのポート

def main():
    p = subprocess.Popen(["./start-julius.sh"], stdout=subprocess.PIPE, shell=True)  # julius起動スクリプトを実行
    pid = str(p.pid)  # juliusのプロセスID取得
    print ('process check : pid = ' + pid)
    time.sleep(5)  # 5秒スリープ
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))  # juliusに接続
    print ('clienet connected')

    try:
        data = ''  # dataの初期化
        print('MainLoop Start')
        time.sleep(5)
        while 1:
            # "/RECOGOUT"を受信するまで、一回分の音声データを全部読み込む。
            while (string.find(data, "\n.") == -1):
                data = data + sock.recv(1024)

            # 音声XMLデータから、<WORD>を抽出して音声テキスト文に連結する。
            strTemp = ""
            for line in data.split('\n'):
                index = line.find('WORD="')
                if index != -1:
                    line = line[index + 6:line.find('"',index + 6)]
                    if line != "[s]":
                        strTemp = strTemp + line

            if strTemp == "よつゆ":
                print("よつゆ")
                subprocess.call("mplayer -vo null -ao alsa:device=hw=1.0 ~/julius/yotsuyu_henji.mp3", shell=True)
            elif strTemp == "こんばんは":
                print("こんばんは")
                subprocess.call("mplayer -vo null -ao alsa:device=hw=1.0 ~/julius/yotsuyu_konbanha.mp3", shell=True)
            else:
                print (strTemp)  # wordを表示
                data = ''  # dataの初期化

            data = ""

    except KeyboardInterrupt:
        print ("KeyboardInterrupt occured.")
        p.kill()
        subprocess.call(["kill " + pid], shell=True)  # juliusのプロセス終了。
        sock.close()

if __name__ == "__main__":
    main()
