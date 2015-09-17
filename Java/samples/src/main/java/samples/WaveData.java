package samples;

import java.util.Calendar;
import java.util.GregorianCalendar;

public class WaveData {

	private int order;
	private double tau;
	private double radians;

	private double sin;
	private double cos;
	private double tan;
	private double sinh;
	private double cosh;
	private double tanh;

	public int getOrder() {
		return order;
	}



	public void setOrder(int order) {
		this.order = order;
	}



	public double getTau() {
		return tau;
	}



	public void setTau(double tau) {
		this.tau = tau;
	}



	public double getRadians() {
		return radians;
	}



	public void setRadians(double radians) {
		this.radians = radians;
	}



	public double getSin() {
		return sin;
	}



	public void setSin(double sin) {
		this.sin = sin;
	}



	public double getCos() {
		return cos;
	}



	public void setCos(double cos) {
		this.cos = cos;
	}



	public double getTan() {
		return tan;
	}



	public void setTan(double tan) {
		this.tan = tan;
	}



	public double getSinh() {
		return sinh;
	}



	public void setSinh(double sinh) {
		this.sinh = sinh;
	}



	public double getCosh() {
		return cosh;
	}



	public void setCosh(double cosh) {
		this.cosh = cosh;
	}



	public double getTanh() {
		return tanh;
	}



	public void setTanh(double tanh) {
		this.tanh = tanh;
	}




	public WaveData()
	{
	}

	public WaveData(double multiplier,double  radians,int order ){

		this.order = order;
		this.radians = radians;
		this.tau = radians / (2 * Math.PI);
		this.sin = multiplier * Math.sin(radians);
		this.cos = multiplier * Math.cos(radians);
		this.tan = multiplier * Math.tan(radians);
		this.sinh = multiplier * Math.sinh(radians);
		this.cosh = multiplier * Math.cosh(radians);
		this.tanh = multiplier * Math.tanh(radians);

	}



	public static WaveData next(int interval, double multiplier, int order){

		Calendar cal =  new GregorianCalendar();

		double sec =  seconds(cal);

		double radians = ((sec % interval) / interval ) * 2 * Math.PI;

		return new WaveData(multiplier, radians, order);


	}



	public static double seconds (Calendar cal){

		double sec = 0; 
		sec += cal.get(Calendar.HOUR_OF_DAY)* 60 * 60;

		sec += cal.get(Calendar.MINUTE) * 60;

		sec += cal.get(Calendar.SECOND);

		sec += cal.get(Calendar.MILLISECOND) / 1000;

		return sec;
	}


	@Override
	public String toString(){

		StringBuilder builder = new StringBuilder();
		builder.append("Order   = " + order);
		builder.append("Radians = " +  radians);
		builder.append("Tau     = "+ tau);
		builder.append("Sine    = "+ sin);
		builder.append("Cosine  = "+ cos);
		builder.append("Tangent = "+ tan);
		builder.append("Sinh    = "+ sinh);
		builder.append("Cosh    = "+ cosh);
		builder.append("Tanh    = "+ tanh);
		return builder.toString();



	}



}
