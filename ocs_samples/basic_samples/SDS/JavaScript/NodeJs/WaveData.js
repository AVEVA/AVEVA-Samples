// WaveData.js
//

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
    
    WaveDataCompound: function() {
        this.Order = null;
        this.Multiplier = null;
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
        
        radians = order * Math.PI/32 +1;

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
    },
    
    // creates a new wave event
    NextWaveCompound: function(order, multiplier) {
        radians = order * 2 * Math.PI;

        newWave = new this.WaveDataCompound();        
        newWave.Order = order;
        newWave.Multiplier = multiplier;
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
