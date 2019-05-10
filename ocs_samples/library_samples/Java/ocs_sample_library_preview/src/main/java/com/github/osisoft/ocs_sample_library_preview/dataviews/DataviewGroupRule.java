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

/**
 * DataviewGroupRule
 */
public class DataviewGroupRule {

    private String Id = "";
    private String Type = "";
    private Object TokenRules= "";

    /**
     * base constructor
     */
    public DataviewGroupRule()
    {
    }

    /**
     * creates a DataviewGroupRule
     * @param Id  
     * @param Type
     */
    public DataviewGroupRule(String Id, String Type)
    {
        this.Id = Id;
        this.Type = Type;
    }    

    /**
     * gets id
     * @return
     */
    public String getId() {
        return Id;
    }

    /**
     * sets id
     * @param id
     */
    public void setId(String id) {
        this.Id = id;
    }

    /**
     * gets type
     * @return
     */
    public String getType() {
        return Type;
    }

    /**
     * sets type
     * @param type
     */
    public void setType(String type) {
        this.Type = type;
    }

    /**
     * get token rule
     * @return
     */
    public Object getTokenRules() {
        return TokenRules;
    }

    /**
     * sets token rule
     * @param tokenRules
     */
    public void setTokenRules(Object tokenRules) {
        this.TokenRules = tokenRules;
    }
}
