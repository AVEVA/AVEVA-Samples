// WaveData.js
//
//Copyright 2019 OSIsoft, LLC
//
//Licensed under the Apache License, Version 2.0 (the "License");
//you may not use this file except in compliance with the License.
//You may obtain a copy of the License at
//
//<http://www.apache.org/licenses/LICENSE-2.0>
//
//Unless required by applicable law or agreed to in writing, software
//distributed under the License is distributed on an "AS IS" BASIS,
//WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//See the License for the specific language governing permissions and
//limitations under the License.

module.exports = {
    // Wave Data Object
    WaveData: function() {
        this.Order = null;
        this.Radians = null;
        this.Tau = null;
        this.Sin = null;
        this.Cos = null;
        this.Tan = null;
        this.Sinh = null;
        this.Cosh = null;
        this.Tanh = null;
    },

    // creates a new wave event
    NextWave: function(interval, multiplier, order) {
        now = new Date();
        midnight = new Date();
        midnight.setHours(0, 0, 0, 0);
        totalSecondsDay = (now -
            midnight);
        _interval = (interval - midnight);
        radians = ((totalSecondsDay % _interval) / _interval) * 2 * Math.PI;

        newWave = new this.WaveData();
        newWave.Order = order;
        newWave.Radians = radians;
        newWave.Tau = radians / (2 * Math.PI);
        newWave.Sin = multiplier * Math.sin(radians);
        newWave.Cos = multiplier * Math.cos(radians);
        newWave.Tan = multiplier * Math.tan(radians);
        newWave.Sinh = multiplier * Math.sinh(radians);
        newWave.Cosh = multiplier * Math.cosh(radians);
        newWave.Tanh = multiplier * Math.tanh(radians);

        return newWave;
    }
}
