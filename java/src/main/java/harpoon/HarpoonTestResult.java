package harpoon;

import org.browsermob.core.har.Har;
import org.codehaus.jackson.map.ObjectMapper;

import java.io.IOException;
import java.io.Writer;
import java.util.Date;

public class HarpoonTestResult {
    private String apiKey;
    private String name;
    private String description;
    private Har har;

    private HarpoonTestResultError error;

    private boolean success;
    private Date created;

    public Har getHar() {
        return har;
    }

    public void setHar(Har har) {
        this.har = har;
    }

    public HarpoonTestResultError getError() {
        return error;
    }

    public void setError(HarpoonTestResultError error) {
        this.error = error;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public Date getCreated() {
        return created;
    }

    public void setCreated(Date created) {
        this.created = created;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void writeTo(Writer writer) throws IOException {
        ObjectMapper om = new ObjectMapper();
        om.writeValue(writer, this);
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getApiKey() {
        return apiKey;
    }

    public void setApiKey(String apiKey) {
        this.apiKey = apiKey;
    }
}
