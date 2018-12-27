/** SdsDatagroup.java
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
import java.util.Map;

public class SdsDatagroup {
    
    private Map<String,Map<String,String>> Tokens;
    private Map<String,Map<String,Object>> DataItems;

    public Map<String,Map<String,String>>  getTokens() {
        return Tokens;
    }

    public void setTokens(Map<String,Map<String,String>> tokens) {
        this.Tokens = tokens;
    }
    

    public Map<String,Map<String,Object>> getDataItems() {
        return DataItems;
    }

    public void setDataItems(Map<String,Map<String,Object>> dataItems) {
        this.DataItems = dataItems;
    }
}
