/** WaveDataInteger.java
 * 
 */

package com.github.osisoft.sdsjava;

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
