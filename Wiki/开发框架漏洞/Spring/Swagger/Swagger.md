# Swagger-UI 漏洞利用

## 利用条件：

- Spring Swagger

## 利用方法：

#### 步骤一：
	
根据Spring的小绿叶logo，或者页面报错 ` Whitelabel Error Page `,有很大可能是Swagger UI的站。
使用 burp [遍历Swagger UI路径]()，当一级目录不存在时，尝试拼接二级目录，通过返回包查看完整数据。

⚠️重点关注：``` /api-docs ``` ｜ ``` /doc.html ``` ｜ ``` /swagger-ui.html ``` ｜ ``` /swagger-resources ``` | ``` /druid ```

![](https://github.com/user-error-404/WIKI-POC/blob/main/Wiki/开发框架漏洞/SpringBoot/Swagger/image/WhitelableErrorPage.png)

#### 步骤二：

直接在 ` Swagger UI ` 页面构造参数发包，接口中有详细的参数介绍.

![](https://github.com/user-error-404/WIKI-POC/blob/main/Wiki/开发框架漏洞/SpringBoot/Swagger/image/SwaggerUI1.png)

![](https://github.com/user-error-404/WIKI-POC/blob/main/Wiki/开发框架漏洞/SpringBoot/Swagger/image/SwaggerUI2.jpg)

#### 步骤三：
	
1. 文件上传接口
	搜索关键字：``` upload ``` 	⚠️重点关注 ``` temp、test ``` 类的上传接口

2. 任意文件下载接口
	搜索关键字：``` downLoad filename path ```

3. SQL注入接口
	接口中的参数

4. 未授权访问接口、任意用户密码重置接口、任意用户信息修改接口、用户信息泄漏接口

## 漏洞原理：