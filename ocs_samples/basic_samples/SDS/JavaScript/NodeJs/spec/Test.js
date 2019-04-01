describe("Sds", function() {
  var Sample = require('../Sample');

  beforeEach(function() {
  });

  it("should be able to complete the main method", function() {
    console.log(Sample);
    sample = Sample(null, null).then(response => {
      v = true;
      console.log(response);
    }).catch(function (err) { 
      console.log(err); 
    });
  });

});
