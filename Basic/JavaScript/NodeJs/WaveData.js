// WaveData.js
//
// Copyright (C) 2018 OSIsoft, LLC. All rights reserved.
//
// THIS SOFTWARE CONTAINS CONFIDENTIAL INFORMATION AND TRADE SECRETS OF
// OSIsoft, LLC.  USE, DISCLOSURE, OR REPRODUCTION IS PROHIBITED WITHOUT
// THE PRIOR EXPRESS WRITTEN PERMISSION OF OSIsoft, LLC.
//
// RESTRICTED RIGHTS LEGEND
// Use, duplication, or disclosure by the Government is subject to restrictions
// as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and
// Computer Software clause at DFARS 252.227.7013
//
// OSIsoft, LLC
// 1600 Alvarado St, San Leandro, CA 94577

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
