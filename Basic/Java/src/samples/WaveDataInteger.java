<# WaveDataInteger.java

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

public class WaveDataInteger {

    private int OrderTarget;
    private int SinInt;
    private int CosInt;
    private int TanInt;


    public WaveDataInteger() {
    }

    public int getOrderTarget() {
        return OrderTarget;
    }

    public void setOrderTarget(int orderTarget) {
        this.OrderTarget = orderTarget;
    }

    public int getSinInt() {
        return SinInt;
    }

    public void setSinInt(int sinInt) {
        this.SinInt = sinInt;
    }

    public int getCosInt() {
        return CosInt;
    }

    public void setCosInt(int cosInt) {
        this.CosInt = cosInt;
    }

    public int getTanInt() {
        return TanInt;
    }

    public void setTanInt(int tanInt) {
        this.TanInt = tanInt;
    }


    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        builder.append("  OrderTarget: " + OrderTarget);
        builder.append(", SinInt: " + SinInt);
        builder.append(", CosInt: " + CosInt);
        builder.append(", TanInt: " + TanInt);

        return builder.toString();
    }
}
