/** WaveDataInteger.java
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
