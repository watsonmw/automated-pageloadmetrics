import org.junit.Test;

public class CaptureHAR extends HarpoonTest
{
    @Test
    public void test_pageLoadTime() throws Exception {
        AssertTimer timer = new AssertTimer();
        driver.get("http://www.webmetrics.com");
        timer.assertLessThen("www.webmetrics.com", 30000);
    }
}