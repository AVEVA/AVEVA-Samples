/** SdsDataviewMapping.java
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


public class SdsDataviewMapping {

    private String IsDefault = "";
    private SdsDataviewMappingColumn[] Columns;

    public String getIsDefault() {
        return IsDefault;
    }

    public void setIsDefault(String isDefault) {
        this.IsDefault = isDefault;
    }

    public SdsDataviewMappingColumn[] getColumns() {
        return Columns;
    }

    public void setColumns(SdsDataviewMappingColumn[] columns) {
        this.Columns = columns;
    }
}
