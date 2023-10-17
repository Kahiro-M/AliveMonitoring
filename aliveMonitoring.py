import configparser
import requests
import time
import subprocess
from datetime import datetime, timedelta, timezone
import argparse
import re

# タイムゾーン指定
JST = timezone(timedelta(hours=+9), 'JST')
def main(interval=5):
    # 設定ファイルから情報を読み取る
    config = configparser.ConfigParser()
    config.read('.\\setting.ini', 'UTF-8')

    while True:
        for section in config.sections():
            if 'IP' in config[section]:
                ip_address = config[section]['IP']
                check_ip_status(section, ip_address)
            elif 'URL' in config[section]:
                url = config[section]['URL']
                check_url_status(section, url)
            else:
                print(f"セクション '{section}' の設定が無効です。")

        # X秒ごとに状態を監視
        time.sleep(interval)

def check_ip_status(name, ip_address):
    # IPアドレスの状態を確認するコードをここに追加
    try:
        # pingコマンドを実行
        result = subprocess.run(["ping", ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # pingの結果を解析
        if "パケット数: 送信 = 4、受信 = 4" in result.stdout.decode(encoding='CP932'):
            print(f"{datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S')}  [{name}] : IPアドレス {ip_address} は正常です。")
        else:
            print(f"{datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S')}  [{name}] : IPアドレス {ip_address} に問題があります。")
    except subprocess.CalledProcessError:
        print(f"{datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S')}  [{name}] : IPアドレス {ip_address} にアクセスできません。")
    except Exception as e:
        print(f"{datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S')}  [{name}] : IPアドレス {ip_address} の状態を確認中にエラーが発生しました。エラー: {str(e)}")


    # 例：pingを使用してIPアドレスに対する状態を確認

def check_url_status(name, url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"{datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S')}  [{name}] : URL {url} は正常です。")
        else:
            print(f"{datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S')}  [{name}] : URL {url} に問題があります。HTTPステータスコード: {response.status_code}")
    except Exception as e:
        print(f"{datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S')}  [{name}] : URL {url} にアクセスできません。エラー: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interval', default=5)
    args = parser.parse_args()
    if(args.interval != None and len(re.findall(r'^\d$', args.interval)) > 0):
        main(int(args.interval))
    else:
        main()
