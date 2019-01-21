/** SdsError.java
 * 
 *  Copyright (C) 2018 OSIsoft, LLC. All rights reserved.
 * 
 *  THIS SOFTWARE CONTAINS CONFIDENTIAL INFORMATION AND TRADE SECRETS OF
 *  OSIsoft, LLC.  USE, DISCLOSURE, OR REPRODUCTION IS PROHIBITED WITHOUT
 *  THE PRIOR EXPRESS WRITTEN PERMISSION OF OSIsoft, LLC.
 * 
 *  RESTRICTED RIGHTS LEGEND
 *  Use, duplication, or disclosure by the Government is subject to restrictions
 *  as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and
 *  Computer Software clause at DFARS 252.227.7013
 * 
 *  OSIsoft, LLC
 *  1600 Alvarado St, San Leandro, CA 94577
 */

package samples;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class SdsError extends Exception {
    private static final long serialVersionUID = 1L;
    private int httpStatusCode;
    private StringBuffer httpErrorMessage;
    private String sdsErrorMessage;

    public SdsError(java.net.HttpURLConnection urlConnection, String msg) {
        String inputLine;
        this.sdsErrorMessage = msg;
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

    public String getSdsErrorMessage() {
        return sdsErrorMessage;
    }

    public void setSdsErrorMessage(String sdsErrorMessage) {
        this.sdsErrorMessage = sdsErrorMessage;
    }
}
