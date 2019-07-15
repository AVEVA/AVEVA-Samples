/** WaveData.java
 * 
 *  Copyright 2019 OSIsoft, LLC
 *  
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *  
 *  http://www.apache.org/licenses/LICENSE-2.0>
 *  
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

package com.github.osisoft.sdsjava;

import java.util.Calendar;
import java.util.GregorianCalendar;

public class WaveData {

    private int Order;
    private double Tau;
    private double Radians;
    private double Sin;
    private double Cos;
    private double Tan;
    private double Sinh;
    private double Cosh;
    private double Tanh;

    public WaveData() {
    }

    public WaveData(double multiplier, double radians, int order) {
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

    public static WaveData next(int interval, double multiplier, int order) {
        double radians = order * (Math.PI / 32);

        return new WaveData(multiplier, radians, order);
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
