# Zabbix SSO认证绕过漏洞

## 利用条件：

- 影响版本：5.4.0 – 5.4.8 或者 6.0.0alpha1
- 启用 SAML SSO 身份验证
- 知道 Zabbix 用户的用户名

## 利用方法：

#### 步骤一：
访问首页获取set-cookie中zbx_session参数的值

#### 步骤二：
通过Url解码和Base64解码获得zbx_session参数Json格式数据

#### 步骤三：
在解码得到的Json中添加`"saml_data":{"username_attribute":"Admin"},`参数后重新Base64编码和Url编码构造Payload

#### 步骤四：
请求index_sso.php，在http请求头中将zbx_session的值替换为url编码后的payload

## 漏洞原理：
在启用 SAML SSO 身份验证（非默认）的情况下，恶意行为者可以修改会话数据，因为存储在会话中的用户登录未经过验证。未经身份验证的恶意攻击者可能会利用此问题来提升权限并获得对 Zabbix 前端的管理员访问权限。

## 修复方法：
1. 禁用SAML身份验证
2. 打厂商已发布升级补丁