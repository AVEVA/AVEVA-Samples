package samples;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class QiError extends Exception {
    private static final long serialVersionUID = 1L;
    private int httpStatusCode;
    private StringBuffer httpErrorMessage;
    private String qiErrorMessage;

    public QiError(java.net.HttpURLConnection urlConnection, String msg) {
        String inputLine;
        this.qiErrorMessage = msg;
        this.httpErrorMessage = new StringBuffer();

        try {
            this.httpStatusCode = urlConnection.getResponseCode();

            if (urlConnection.getErrorStream() != null) {
                BufferedReader in = new BufferedReader(
                        new InputStreamReader(urlConnection.getErrorStream()));

                while ((inputLine = in.readLine()) != null) {
                    this.httpErrorMessage.append(inputLine);
                }
                in.close();
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public int getHttpStatusCode() {
        return httpStatusCode;
    }

    public void setHttpStatusCode(int httpStatusCode) {
        this.httpStatusCode = httpStatusCode;
    }

    public StringBuffer getHttpErrorMessage() {
        return httpErrorMessage;
    }

    public void setHttpErrorMessage(StringBuffer httpErrorMessage) {
        this.httpErrorMessage = httpErrorMessage;
    }

    public String getQiErrorMessage() {
        return qiErrorMessage;
    }

    public void setQiErrorMessage(String qiErrorMessage) {
        this.qiErrorMessage = qiErrorMessage;
    }
}
