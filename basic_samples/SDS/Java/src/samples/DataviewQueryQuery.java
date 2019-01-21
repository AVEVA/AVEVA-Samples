/** DataviewQueryQuery.java
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


public class DataviewQueryQuery {

    private String Type = "";
    private String Value = "";
    private String Operator = "";

    public String getType() {
        return Type;
    }

    public void setType(String type) {
        this.Type = type;
    }

    public String getValue() {
        return Value;
    }

    public void setValue(String value) {
        this.Value = value;
    }

    public String getOperator() {
        return Operator;
    }

    public void setOperator(String operator) {
        this.Operator = operator;
    }
}
