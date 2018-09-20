<# SdsViewMap.java

   Copyright (C) 2018 OSIsoft, LLC. All rights reserved.

   THIS SOFTWARE CONTAINS CONFIDENTIAL INFORMATION AND TRADE SECRETS OF
   OSIsoft, LLC.  USE, DISCLOSURE, OR REPRODUCTION IS PROHIBITED WITHOUT
   THE PRIOR EXPRESS WRITTEN PERMISSION OF OSIsoft, LLC.

   RESTRICTED RIGHTS LEGEND
   Use, duplication, or disclosure by the Government is subject to restrictions
   as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and
   Computer Software clause at DFARS 252.227.7013

   OSIsoft, LLC
   1600 Alvarado St, San Leandro, CA 94577
#>

package samples;


public class SdsViewMap {

    private String SourceTypeId = "";
    private String TargetTypeId = "";
    private SdsViewProperty[] Properties = new SdsViewProperty[0];

    public String getSourceTypeId() {
        return this.SourceTypeId;
    }

    public void setSourceTypeId(String sourceTypeId) {
        this.SourceTypeId = sourceTypeId;
    }
    
    public String getTargetTypeId() {
        return TargetTypeId;
    }

    public void setTargetTypeId(String targetTypeId) {
        this.TargetTypeId = targetTypeId;
    }

    public SdsViewProperty[] getProperties() {
        return Properties;
    }

    public void setProperties(SdsViewProperty[] properties) {
        this.Properties = properties;
    }
    
    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        builder.append("  SourceId = " + SourceTypeId);
        builder.append(", TargetId = " + TargetTypeId);        
        for(SdsViewProperty prop: Properties)
        {
        	if(prop.getTargetId() != null)
        	{
        	 builder.append(", SdsViewProperty: " + prop.getSourceId() + " => " + prop.getTargetId());
        	}
        }
       
        return builder.toString();
    }
}
