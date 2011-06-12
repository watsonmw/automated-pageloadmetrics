import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.firefox.FirefoxDriver;

public class PageLoadTime
{
    @Test
    public void test_googleCheese() throws Exception {
        FirefoxDriver driver = new FirefoxDriver();
        AssertTimer timer = new AssertTimer();
        driver.get("http://www.google.com");
        WebElement element = driver.findElement(By.name("q"));
        element.sendKeys("Cheese!");
        element.submit();
        timer.assertLessThen(18000);
    }
}