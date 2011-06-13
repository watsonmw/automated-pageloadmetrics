import org.junit.Test;
import org.junit.runner.RunWith;
import org.openqa.selenium.By;

@RunWith(HarpoonTestRunner.class)
public class Bandwidth extends HarpoonTest
{
    @Test
    public void test_pageLoadTime() throws Exception {
        proxy.blacklistRequests("http(s)?://[^.]+\\\\.google-analytics\\\\.com/.*", 202);
        proxy.blacklistRequests("http(s)?://[^.]+\\\\.google-analytics\\\\.com/.*", 202);
        AssertTimer timer = new AssertTimer();
        driver.get("http://blip.fm/all");
        timer.assertLessThen("blip.fm load time", 30000);
    }

    @Test
    public void test_pageLoadTimeBandwithLimit() throws Exception {
        proxy.blacklistRequests("http(s)?://[^.]+\\\\.google-analytics\\\\.com/.*", 202);
        proxy.blacklistRequests("http(s)?://[^.]+\\\\.google-analytics\\\\.com/.*", 202);
        proxy.setUpstreamKbps(20);
        proxy.setDownstreamKbps(80);
        AssertTimer timer = new AssertTimer();
        driver.get("http://blip.fm/all");
        driver.findElement(By.id("tagTunerDisplayToggle")).click();
        timer.assertLessThen("blip fm load time - bandwidth limited", 60000);
    }
}