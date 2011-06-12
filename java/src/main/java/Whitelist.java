import org.junit.Test;
import org.junit.runner.RunWith;
import org.openqa.selenium.By;

@RunWith(HarpoonTestRunner.class)
public class Whitelist extends HarpoonTest
{
    @Test
    public void test_pageLoadTime() throws Exception {
        AssertTimer timer = new AssertTimer();
        driver.get("http://webmetrics.com");
        timer.assertLessThen("webmetrics.com load time", 30000);
    }

    @Test
    public void test_pageLoadTimeNoExternalContent() throws Exception {
        String whitelist[] = {
          "http(s)?://[^.]+\\\\.webmetrics.com\\\\.com/.*"
        };
        proxy.whitelistRequests(whitelist, 202);
        AssertTimer timer = new AssertTimer();
        driver.get("http://webmetrics.com");
        timer.assertLessThen("webmetrics.com load time - no external content", 30000);
    }
}