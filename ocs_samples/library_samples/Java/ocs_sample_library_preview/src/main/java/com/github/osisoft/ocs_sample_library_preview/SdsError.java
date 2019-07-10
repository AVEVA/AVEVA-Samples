/** SdsError.java
 * 
 */

package com.github.osisoft.ocs_sample_library_preview;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

/**
 * Helper for exceptions
 */
public class SdsError extends Exception {
    private static final long serialVersionUID = 1L;
    private int httpStatusCode;
    private StringBuffer httpErrorMessage;
    private String sdsErrorMessage;
    private String url;

    /**
     * USe this to just send a message in an exception
     * @param msg message to send
     */
    public SdsError(String msg) {
        this.sdsErrorMessage = msg;
    }

    /**
     * if support is needed please know the Operation-ID header information for (it is included in the exception below automatically too)
     * 
     * Use this to capture an OCS action error
     * @param urlConnection the failed action
     * @param msg message to help illuminate the issue
     */
    public SdsError(java.net.HttpURLConnection urlConnection, String msg) {
        String inputLine;
        this.sdsErrorMessage = msg;
        this.httpErrorMessage = new StringBuffer();

        try {
            this.httpStatusCode = urlConnection.getResponseCode();
            this.url = urlConnection.getURL().toString();

            if (urlConnection.getErrorStream() != null) {
                BufferedReader in = new BufferedReader(
                        new InputStreamReader(urlConnection.getErrorStream(), StandardCharsets.UTF_8));

                while ((inputLine = in.readLine()) != null) {
                    this.httpErrorMessage.append(inputLine);
                }
                in.close();
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * gets the status code associated with the OCS based issue
     * @return httpStatusCode
     */
    public int getHttpStatusCode() {
        return httpStatusCode;
    }

    /**
     * If you need to set the status code manually
     * @param httpStatusCode status code
     */
    public void setHttpStatusCode(int httpStatusCode) {
        this.httpStatusCode = httpStatusCode;
    }

    /**
     * Get the http error message directly
     * @return error message
     */
    public StringBuffer getHttpErrorMessage() {
        return httpErrorMessage;
    }

    /**
     * set the http error message directly
     * @param httpErrorMessage error message
     */
    public void setHttpErrorMessage(StringBuffer httpErrorMessage) {
        this.httpErrorMessage = httpErrorMessage;
    }

    /**
     * gets the sds error message directly.  this is used to explain the error
     * @return the error message
     */
    public String getSdsErrorMessage() {
        return sdsErrorMessage;
    }

    /**
     * sets the sds error message directly.  Use this to explain the error
     * @param sdsErrorMessage
     */
    public void setSdsErrorMessage(String sdsErrorMessage) {
        this.sdsErrorMessage = sdsErrorMessage;
    }

    /**
     * prints the exception in an easier to read format
     */
    public void print() {
        System.out.println("SdsError Msg: " + this.getSdsErrorMessage());
        if(httpErrorMessage !=null)
        {
            System.out.println("HttpStatusCode: " + this.getHttpStatusCode());
            System.out.println("errorMessage: " + this.getMessage());
            System.out.println("httpErrorMessage: " + this.httpErrorMessage.toString());
            System.out.println("url: " + this.url.toString());
        }
    }  
}
