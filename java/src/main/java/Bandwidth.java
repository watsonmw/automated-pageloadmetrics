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
        timer.assertLessThen("main page", 30000);
    }

    //@Test
    public void test_tagTuner() throws Exception {
        AssertTimer timer = new AssertTimer();
        driver.get("http://blip.fm/all");
        driver.findElement(By.id("tagTunerDisplayToggle")).click();
        timer.assertLessThen("login page", 30000);
    }
}