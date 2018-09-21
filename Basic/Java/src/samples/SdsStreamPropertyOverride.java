/** SdsStreamPropertyOverride.java
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

public class SdsStreamPropertyOverride {
    private String sdsTypePropertyId;
    private SdsInterpolationMode interpolationMode;
    private String uom;
    
    public SdsStreamPropertyOverride() {

    }

    public String getSdsTypePropertyId() {
        return sdsTypePropertyId;
    }

    public void setSdsTypePropertyId(String sdsTypePropertyId) {
        this.sdsTypePropertyId = sdsTypePropertyId;
    }

    public SdsInterpolationMode getInterpolationMode() {
        return interpolationMode;
    }

    public void setInterpolationMode(SdsInterpolationMode interpolationMode) {
        this.interpolationMode = interpolationMode;
    }
    
    public String getUom() {
        return uom;
    }

    public void setUom(String uom) {
        this.uom = uom;
    }
}
