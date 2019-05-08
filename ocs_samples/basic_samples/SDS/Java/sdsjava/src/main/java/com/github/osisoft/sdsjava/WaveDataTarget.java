/** WaveDataTarget.java
 * 
 */

package com.github.osisoft.sdsjava;

public class WaveDataTarget {

    private int OrderTarget;
    private double TauTarget;
    private double RadiansTarget;
    private double SinTarget;
    private double CosTarget;
    private double TanTarget;
    private double SinhTarget;
    private double CoshTarget;
    private double TanhTarget;

    public WaveDataTarget() {
    }


    public int getOrderTarget() {
        return OrderTarget;
    }

    public void setOrderTarget(int orderTarget) {
        this.OrderTarget = orderTarget;
    }

    public double getTauTarget() {
        return TauTarget;
    }

    public void setTauTarget(double tauTarget) {
        this.TauTarget = tauTarget;
    }

    public double getRadiansTarget() {
        return RadiansTarget;
    }

    public void setRadiansTarget(double radiansTarget) {
        this.RadiansTarget = radiansTarget;
    }

    public double getSinTarget() {
        return SinTarget;
    }

    public void setSinTarget(double sinTarget) {
        this.SinTarget = sinTarget;
    }

    public double getCosTarget() {
        return CosTarget;
    }

    public void setCosTarget(double cosTarget) {
        this.CosTarget = cosTarget;
    }

    public double getTanTarget() {
        return TanTarget;
    }

    public void setTanTarget(double tanTarget) {
        this.TanTarget = tanTarget;
    }

    public double getSinhTarget() {
        return SinhTarget;
    }

    public void setSinhTarget(double sinhTarget) {
        this.SinhTarget = sinhTarget;
    }

    public double getCoshTarget() {
        return CoshTarget;
    }

    public void setCoshTarget(double coshTarget) {
        this.CoshTarget = coshTarget;
    }

    public double getTanhTarget() {
        return TanhTarget;
    }

    public void setTanhTarget(double tanhTarget) {
        this.TanhTarget = tanhTarget;
    }

    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        builder.append("OrderTarget: " + OrderTarget);
        builder.append(", RadiansTarget: " + RadiansTarget);
        builder.append(", TauTarget: " + TauTarget);
        builder.append(", SinTarget: " + SinTarget);
        builder.append(", CosTarget: " + CosTarget);
        builder.append(", TanTarget: " + TanTarget);
        builder.append(", SinhTarget: " + SinhTarget);
        builder.append(", CoshTarget: " + CoshTarget);
        builder.append(", TanhTarget: " + TanhTarget);
        return builder.toString();
    }
}
