import harpoon.HarpoonTestResult;
import harpoon.HarpoonTestResultError;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.HttpVersion;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.params.CoreProtocolPNames;
import org.apache.http.util.EntityUtils;
import org.browsermob.core.har.Har;
import org.junit.runners.BlockJUnit4ClassRunner;
import org.junit.runners.model.FrameworkMethod;
import org.junit.runners.model.InitializationError;
import org.junit.runners.model.Statement;

import java.io.IOException;
import java.io.StringWriter;
import java.util.Date;

public class HarpoonTestRunner extends BlockJUnit4ClassRunner {
    private HarpoonTest test;
    private HarpoonTestResult result = new HarpoonTestResult();

    public HarpoonTestRunner(Class<?> klass) throws InitializationError {
        super(klass);
    }

    @Override
    protected Statement methodInvoker(final FrameworkMethod method, final Object oTest) {
        final String displayName = describeChild(method).getDisplayName();

        this.test = (HarpoonTest) oTest;

        return new Statement() {
            @Override
            public void evaluate() throws Throwable {
                try {
                    method.invokeExplosively(test);
                    result.setSuccess(true);
                } catch (Throwable throwable) {
                    result.setSuccess(false);

                    HarpoonTestResultError error = new HarpoonTestResultError();
                    error.setMessage(throwable.toString());
                    result.setError(error);

                    throw throwable;
                } finally {
                    Har har = test.getProxy().getHar();
                    if (null != har) {
                        result.setHar(har);
                        if (har.getLog() != null && har.getLog().getEntries().size() > 0) {
                            String url = har.getLog().getEntries().get(0).getRequest().getUrl();
                            result.setDescription(url);
                        }

                        result.setName(displayName);
                        result.setCreated(new Date());

                        postTestResults(result);
                    }
                }
            }
        };
    }

    private void postTestResults(HarpoonTestResult result) throws IOException {
        HttpClient httpclient = new DefaultHttpClient();
        httpclient.getParams().setParameter(CoreProtocolPNames.PROTOCOL_VERSION, HttpVersion.HTTP_1_1);

        HttpPost httppost = new HttpPost("http://labs.webmetrics.com:8080/test-results");

        StringWriter stringWriter = new StringWriter();
        result.writeTo(stringWriter);
        StringEntity reqEntity = new StringEntity(stringWriter.toString());

        httppost.setEntity(reqEntity);
        //reqEntity.setContentType("text/json");
        System.out.println("executing request " + httppost.getRequestLine());
        HttpResponse response = httpclient.execute(httppost);
        HttpEntity resEntity = response.getEntity();

        System.out.println(response.getStatusLine());
        if (resEntity != null) {
          System.out.println(EntityUtils.toString(resEntity));
        }
        if (resEntity != null) {
          resEntity.consumeContent();
        }

        httpclient.getConnectionManager().shutdown();
    }
}
