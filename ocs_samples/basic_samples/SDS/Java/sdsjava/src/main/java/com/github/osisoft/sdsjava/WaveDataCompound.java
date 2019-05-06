/** WaveDataCompound.java
 * 
 */

package com.github.osisoft.sdsjava;

import java.util.Calendar;
import java.util.GregorianCalendar;

public class WaveDataCompound {

    private int Order;
    private int Multiplier;
    private double Tau;
    private double Radians;
    private double Sin;
    private double Cos;
    private double Tan;
    private double Sinh;
    private double Cosh;
    private double Tanh;

    public WaveDataCompound() {
    }

    public WaveDataCompound(int multiplier, double radians, int order) {
        this.Multiplier = multiplier;
        this.Order = order;
        this.Radians = radians;
        this.Tau = radians / (2 * Math.PI);
        this.Sin = multiplier * Math.sin(radians);
        this.Cos = multiplier * Math.cos(radians);
        this.Tan = multiplier * Math.tan(radians);
        this.Sinh = multiplier * Math.sinh(radians);
        this.Cosh = multiplier * Math.cosh(radians);
        this.Tanh = multiplier * Math.tanh(radians);
    }

    public static WaveDataCompound next(int order,int multiplier) {
        double radians = (order) * 2 * Math.PI;

        return new WaveDataCompound(multiplier, radians, order);
    }

    public static double seconds(Calendar cal) {
        double sec = 0;
        sec += cal.get(Calendar.HOUR_OF_DAY) * 60 * 60 * 1000;
        sec += cal.get(Calendar.MINUTE) * 60 * 1000;
        sec += cal.get(Calendar.SECOND) * 1000;
        sec += (double) cal.get(Calendar.MILLISECOND);

        return sec;
    }

    public int getOrder() {
        return Order;
    }

    public void setOrder(int order) {
        this.Order = order;
    }

    public int getMultiplier() {
        return Multiplier;
    }

    public void setMultiplier(int multiplier) {
        this.Multiplier = multiplier;
    }

    public double getTau() {
        return Tau;
    }

    public void setTau(double tau) {
        this.Tau = tau;
    }

    public double getRadians() {
        return Radians;
    }

    public void setRadians(double radians) {
        this.Radians = radians;
    }

    public double getSin() {
        return Sin;
    }

    public void setSin(double sin) {
        this.Sin = sin;
    }

    public double getCos() {
        return Cos;
    }

    public void setCos(double cos) {
        this.Cos = cos;
    }

    public double getTan() {
        return Tan;
    }

    public void setTan(double tan) {
        this.Tan = tan;
    }

    public double getSinh() {
        return Sinh;
    }

    public void setSinh(double sinh) {
        this.Sinh = sinh;
    }

    public double getCosh() {
        return Cosh;
    }

    public void setCosh(double cosh) {
        this.Cosh = cosh;
    }

    public double getTanh() {
        return Tanh;
    }

    public void setTanh(double tanh) {
        this.Tanh = tanh;
    }

    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        builder.append("Order: " + Order);
        builder.append(", Multiplier: " + Multiplier);
        builder.append(", Radians: " + Radians);
        builder.append(", Tau: " + Tau);
        builder.append(", Sin: " + Sin);
        builder.append(", Cos: " + Cos);
        builder.append(", Tan: " + Tan);
        builder.append(", Sinh: " + Sinh);
        builder.append(", Cosh: " + Cosh);
        builder.append(", Tanh: " + Tanh);
        return builder.toString();
    }
}
