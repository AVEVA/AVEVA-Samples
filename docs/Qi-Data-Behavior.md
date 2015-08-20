################
Qi Data Behavior
################

Stream Data
===========

A stream is defined as an ordered sequence of values where the order is determined by a primary index. The primary index has a uniqueness constraint and as such only one value can exist for a particular index value within a stream. 
A stream can be defined to contain complex data value but all values within a stream must conform to a single type definition. An example type definition is shown below.
Stream Name	 	 	 
SensorData			 
 	Type Name	 	 
 	SensorValue		 
 	 	Field Name	Field Type
 	 	◊TimeId	DateTime
 	 	Measurement	Double
In this example the TimeId field is denoted as the primary index and as such a stream of SensorValues may only one SensorValue for each unique DateTime value.

***************
Stream Behavior
***************
The value of a stream at any particular index value is determined by the stream behavior. A stream can generally be considered to behave in one of three gross modes, discrete, stepwise continuous, and continuous.

Simple Values
=============
We will examine these behaviors by considering a stream defined with a type definition of SensorValue. To this stream we will add the following distinct values:

+------------------------+------------+
| Time Id                | Measurement|
+========================+============+
| 01-Jan-2010 12:00 PM   | 0          |
+------------------------+------------+
| 01-Jan-2010 12:10 PM   | 4          |
+------------------------+------------+
| 01-Jan-2010 12:20 PM   | 2          |
+------------------------+------------+
| 01-Jan-2010 12:30 PM   | 6          |
+------------------------+------------+
| 01-Jan-2010 12:40 PM   | 2          |
+------------------------+------------+
| 01-Jan-2010 1:0 0 PM   | 12         |
+------------------------+------------+



********
Discrete
********
In the case of a discrete stream it is assumed that there are no values at index locations which have not been explicitly added to the stream. A plot of the stream data is shown below.

.. image:: images/QiDataBehaviorsSimpleDiscrete.PNG

If we considered a data access call to retrieve a SensorValue at an index of 01-Jan-2010 12:50 PM, in the case of a discrete stream the value does not exist.

*******************
Stepwise Continuous
*******************
In the case of stepwise continuous stream it is assumed that the value a stream remains the same for increasing index values until another distinct value is encountered.

.. image:: images/QiDataBehaviorsSimpleStepwiseContinuous1.PNG
 
Again if we considered a data access call to retrieve a SensorValue at an index of 01-Jan-2010 12:50 PM, this time the Measurement field will have a value of 2.
We should note that there is also a variant to this behavior where the value of the stream immediately transitions to the value of next distinct value.
 
.. image:: images/QiDataBehaviorsSimpleStepwiseContinuous2.PNG
In this case the value of the Measurement field of the SensorValue at an index of 01-Jan-2010 12:50 PM will be 12. We will refer to this variant in future as stepwise continuous (trailing edge) and the former as stepwise continuous (leading edge).

**********
Continuous
**********
For a continuous streams we assume that there is a valid value for every possible index value. The actual value between distinct values depends on the algorithm being employed. The plot below demonstrates how the how stream would behave if a linear interpolation method was employed. In this case the value of the Measurement field of the SensorValue at an index of 01-Jan-2010 12:50 PM will be 7.

.. image:: images/QiDataBehaviorsSimpleContinuous.PNG
 
Complex Values
==============
In the previous example we considered a simple type definition with just two fields, an index field and a scalar value field. This example was useful for demonstrating basic stream behaviors but in practice type definitions can be much more complex.
In the following example we will consider a type definition with multiple scalar fields besides the primary index as follows.
Stream Name	 	 	 
SensorData			 
 	Type Name	 	 
 	SensorValue&Status		 
 	 	Field Name	Field Type
 	 	◊TimeId	DateTime
		Measurement	Double
 	 	Status	Int32

We will again examine behaviors by considering a stream with a set of distinct SensorValue & Status values as follows:


+------------------------+------------+------------+
| Time Id                | Measurement| Status     |
+========================+============+============+
| 01-Jan-2010 12:00 PM   | 0          | 1          |
+------------------------+------------+------------+
| 01-Jan-2010 12:10 PM   | 4          | 1          |
+------------------------+------------+------------+
| 01-Jan-2010 12:20 PM   | 2          | 1          |
+------------------------+------------+------------+
| 01-Jan-2010 12:30 PM   | 6          | 0          |
+------------------------+------------+------------+
| 01-Jan-2010 12:40 PM   | 2          | 0          |
+------------------------+------------+------------+
| 01-Jan-2010 1:0 0 PM   | 12         | 1          |
+------------------------+------------+------------+

********
Discrete
********
In the case of a discrete stream the behavior is same as in the case of simple type in that between distinct values, no value exists.

*******************
Stepwise Continuous
*******************
For both stepwise continuous (trailing edge) and stepwise continuous (leading edge) the behavior is again the same as with a simple type because no interpretation of the data in the type fields is required to return a value.

**********
Continuous
**********
In the case of continuous stream there are multiple fields to which an algorithm could to be applied in order to return a SensorValue&Status at an index value. In practice this isn’t always desirable and distinct behaviors typically need to be applied to each of the fields.
In the example below, the default behavior for stream is continuous, but the Status field is interpreted as stepwise continuous (leading edge). Essentially the overall behavior for the stream is continuous but the behavior of the Status field is overridden as stepwise continuous (leading edge).
Stream Name	Behavior	 	 	 	
SensorData	Continuous			 	
 		Type Name	 	 	
 		SensorValue&Status		 	
 		 	Field Name	Field Type	Behavior
 		 	◊TimeId	DateTime	
			Measurement	Double	
 		 	Status	Int32	Stepwise (LE)
If a data access call is made to retrieve a SensorValue&Status at an index of 01-Jan-2010 12:50 PM, a value is returned with a Measurement of 7 and a Status of 0. 

Field Types
===========
The full Qi type specification also allows for field types that are non-numeric so we must consider
