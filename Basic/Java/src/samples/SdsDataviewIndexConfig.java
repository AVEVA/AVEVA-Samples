/** SdsDataviewIndexConfig.java
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


public class SdsDataviewIndexConfig {

    private String IsDefault = "";
    private String StartIndex = "";
    private String EndIndex = "";
    private String Mode = "";
    private String Interval = "";

    public String getIsDefault() {
        return IsDefault;
    }

    public void setIsDefault(String isDefault) {
        this.IsDefault = isDefault;
    }

    public String getStartIndex() {
        return StartIndex;
    }

    public void setStartIndex(String startIndex) {
        this.StartIndex = startIndex;
    }

    public String getEndIndex() {
        return EndIndex;
    }

    public void setEndIndex(String endIndex) {
        this.EndIndex = endIndex;
    }

    public String getMode() {
        return Mode;
    }

    public void setMode(String mode) {
        this.Mode = mode;
    }

    public String getInterval() {
        return Interval;
    }

    public void setInterval(String interval) {
        this.Interval = interval;
    }

}
