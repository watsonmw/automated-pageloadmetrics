import org.junit.Assert;

public class AssertTimer {
    private long startTime = 0;

    public AssertTimer()
    {
        startTime = System.currentTimeMillis();
    }

    public void assertLessThen(long time)
    {
        long timing = System.currentTimeMillis() - startTime;
        startTime = System.currentTimeMillis();
        Assert.assertTrue("Exceeded timeout of " + time + "ms", timing < time);
    }

    public void assertLessThen(String message, long time)
    {
        long timing = System.currentTimeMillis() - startTime;
        startTime = System.currentTimeMillis();
        Assert.assertTrue(message + " exceeded timeout of " + time + "ms", timing < time);
    }
}
