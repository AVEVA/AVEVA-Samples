/** DataviewGroupRule.java
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

package  com.github.osisoft.ocs_sample_library_preview.dataviews;


public class DataviewGroupRule {

    private String Id = "";
    private String Type = "";
    private String TokenRules= "";

    public DataviewGroupRule()
    {
    }

    public DataviewGroupRule(String Id, String Type)
    {
        this.Id = Id;
        this.Type = Type;
    }
    

    public String getId() {
        return Id;
    }

    public void setId(String id) {
        this.Id = id;
    }

    public String getType() {
        return Type;
    }

    public void setType(String type) {
        this.Type = type;
    }

    public String getTokenRules() {
        return TokenRules;
    }

    public void setTokenRules(String tokenRules) {
        this.TokenRules = tokenRules;
    }
}
