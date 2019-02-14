/** SdsError.java
 * 
 *  Copyright 2019 OSIsoft, LLC
 *  
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *  
 *  http://www.apache.org/licenses/LICENSE-2.0>
 *  
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

package  com.github.osisoft.ocs_sample_library_preview;

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

    public void print() {
        System.out.println("SdsError Msg: " + this.getSdsErrorMessage());
        System.out.println("HttpStatusCode: " + this.getHttpStatusCode());
        System.out.println("errorMessage: " + this.getMessage());
        System.out.println("httpErrorMessage: " + this.httpErrorMessage.toString());
    }  
}
