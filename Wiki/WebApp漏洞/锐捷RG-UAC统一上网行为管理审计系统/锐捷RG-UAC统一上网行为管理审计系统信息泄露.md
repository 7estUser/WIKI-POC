# 锐捷RG-UAC统一上网行为管理审计系统信息泄露

## 资产搜索
fofa title="RG-UAC登录页面" && body="admin"

## POC
访问系统url的时候，GET请求响应中会暴露系统存在账号密码信息泄露，F12查看源码获取密码md5值，搜索 `super_admin` 、`password`
![](img/passwd.jpg)