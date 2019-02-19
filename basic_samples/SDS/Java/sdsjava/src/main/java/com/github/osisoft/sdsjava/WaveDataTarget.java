/** WaveDataTarget.java
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
