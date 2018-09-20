<# SdsViewProperty.java

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


public class SdsViewProperty {
    private String SourceId;
    private String TargetId;
    private SdsView SdsView;

    public String getSourceId() {
        return SourceId;
    }

    public void setSourceId(String SourceId) {
        this.SourceId = SourceId;
    }

    public String getTargetId() {
        return TargetId;
    }

    public void setTargetId(String targetId) {
        this.TargetId = targetId;
    }

    public SdsView getSdsView() {
        return SdsView;
    }

    public void setSdsView(SdsView sdsView) {
        this.SdsView = sdsView;
    }
}
