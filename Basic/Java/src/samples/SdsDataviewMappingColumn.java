/** SdsDataviewMappingColumn.java
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

public class SdsDataviewMappingColumn {

    private String Name = "";
    private String IsKey = "";
    private String DataType = "";
    private SdsDataviewMappingRule MappingRule;

    public String getName() {
        return Name;
    }

    public void setName(String name) {
        this.Name = name;
    }

    public String getIsKey() {
        return IsKey;
    }

    public void setIsKey(String isKey) {
        this.IsKey = isKey;
    }

    public String getDataType() {
        return DataType;
    }

    public void setDataType(String dataType) {
        this.DataType = dataType;
    }

    public SdsDataviewMappingRule  getMappingRule() {
        return MappingRule;
    }

    public void setMappingRule(SdsDataviewMappingRule mappingRule) {
        this.MappingRule = mappingRule;
    }
}
