#Config
host = 'portquiz.net'
timeout = 1
rangeMin = 0
rangeMax = 1023

import time
import json
import urllib.request
import socket

def tcpPortScan(host, port, timeout = 10, closeWait = 1):
    ## ソケットの作成
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    try:
        ## 接続開始
        s.connect((host, port))
        status = 'Success'
        time.sleep(closeWait)
        s.close()
    except socket.timeout:
        ## タイムアウト
        status = 'Timeout'
    except socket.error as e:
        ## エラー
        status = 'Error'
    
    ## 終了
    return status

if(input('ポートスキャンを開始しますか?y/n: ') != 'y'):
    exit

method = input('\nネット接続方法は?\nデザリング: 1\n自宅のwifiまたは有線: 2\n学校のwifi: 3\n寮のwifi: 4\nその他: 5\n')
try:
    ip = urllib.request.urlopen('http://checkip.dyndns.com/').read().decode('utf-8')
except:
    ip = 'Error'


## カウント
openCount = 0
timeoutCount = 0
errorCount = 0

## 記録
data = {
    "tcp": [],
    "status": {
        "ip": ip,
        "method": method
    }
}

for port in range(rangeMin, rangeMax + 1):
    ## スキャン
    result = tcpPortScan(host, port, timeout = timeout, closeWait = timeout)

    ## カウント
    if(result == 'Success'):
        openCount = openCount + 1
        showResult = '解放'
    elif(result == 'Timeout'):
        timeoutCount = timeoutCount + 1
        showResult = '閉鎖'
    elif(result == 'Error'):
        errorCount = errorCount + 1
        showResult = 'エラー'

    ## 記録
    data["tcp"].append({"port": port, "result": result})

    ## 表示
    process = round(((port - rangeMin) / (rangeMax - rangeMin)) * 100, 2)
    scanStatus = 'TCP/' + str(rangeMin) + '-' + str(rangeMax) + 'スキャン中! ' + str(process) + '%完了  TCP/'+ str(port) + ' ' + showResult
    portStatus = '解放:' + str(openCount) + ' タイムアウト:' + str(timeoutCount) + ' エラー:' + str(errorCount)
    print('\r' + scanStatus + '    ' + portStatus + '        ', end='')

print('\nポートスキャンが完了しました。')

with open('result.json', mode='wt', encoding='utf-8') as file:
  json.dump(data, file, ensure_ascii=False, indent=2)

print('\nスキャン結果をresult.jsonに保存しました。\nresult.jsonを指定のクラウドにアップロードしてください。\nファイルの内容\n・IPアドレス\n・質問の回答\n・スキャン結果')