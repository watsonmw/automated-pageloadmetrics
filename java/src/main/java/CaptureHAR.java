import org.browsermob.core.har.Har;
import org.browsermob.proxy.ProxyServer;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.ExternalResource;
import org.junit.rules.TestName;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.remote.DesiredCapabilities;

import java.io.File;
import java.io.IOException;
import java.util.Date;

public class CaptureHAR
{
    protected ProxyServer proxy;
    protected WebDriver driver;
    protected String resultsDir;

    @Rule
    public TestName name = new TestName();
    @Rule public ExternalResource setup = new ExternalResource() {
        @Override
        protected void before() throws Throwable {
            proxy = new ProxyServer(9090);
            proxy.start();

            DesiredCapabilities caps = new DesiredCapabilities();
            caps.setCapability("proxy", proxy.seleniumProxy());

            driver = new FirefoxDriver(caps);
            proxy.newHar("Capture Test");
        }

        @Override
        protected void after() {
            // Create the test results dir if it doesn't exist
            if (resultsDir == null) {
                resultsDir = "logs/" + String.valueOf(new Date().getTime()/1000);
            }

            File dir = new File(resultsDir);
            if (!dir.exists()) {
                dir.mkdirs();
            }

            File harFile = new File(dir.getPath() + "/" + name.getMethodName() + ".har");

            proxy.endPage();

            Har har = proxy.getHar();
            try {
                har.writeTo(harFile);
            } catch (IOException e) {
                e.printStackTrace();
            }

            driver.quit();
            try {
                proxy.stop();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    };


    @Test
    public void test_pageLoadTime() throws Exception {
        AssertTimer timer = new AssertTimer();
        driver.get("http://www.webmetrics.com");
        timer.assertLessThen("www.webmetrics.com", 30000);
    }
}