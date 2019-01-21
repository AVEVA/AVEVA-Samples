/** SdsType.java
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


public class SdsType {

    private String Id = "";
    private String Name = "";
    private String Description = "";
    private SdsTypeCode SdsTypeCode;
    private SdsTypeProperty[] Properties = new SdsTypeProperty[0];

    public String getId() {
        return Id;
    }

    public void setId(String id) {
        this.Id = id;
    }

    public String getName() {
        return Name;
    }

    public void setName(String name) {
        this.Name = name;
    }

    public String getDescription() {
        return Description;
    }

    public void setDescription(String description) {
        this.Description = description;
    }

    public SdsTypeCode getSdsTypeCode() {
        return SdsTypeCode;
    }

    public void setSdsTypeCode(SdsTypeCode sdsTypeCode) {
        this.SdsTypeCode = sdsTypeCode;
    }

    public SdsTypeProperty[] getProperties() {
        return Properties;
    }

    public void setProperties(SdsTypeProperty[] properties) {
        this.Properties = properties;
    }
}
