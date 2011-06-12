import org.junit.Test;
import org.junit.runner.RunWith;

@RunWith(HarpoonTestRunner.class)
public class UploadHAR extends HarpoonTest
{
    @Test
    public void test_uploadHAR() throws Exception {
        AssertTimer timer = new AssertTimer();
        driver.get("http://webmetrics.com");
        timer.assertLessThen("www.webmetrics.com", 30000);
    }
}