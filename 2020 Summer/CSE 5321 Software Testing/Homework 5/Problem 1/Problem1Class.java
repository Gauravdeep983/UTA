package Homework5;

public class Problem1Class {

	int pulseCount;
	boolean emerBrake;
	
	public void emerBrakeFunction (boolean cruiseEngaged, double speed, double distance) {
		emerBrake = (cruiseEngaged && (speed>50.0 || distance<=35.0));
		pulseCount = (cruiseEngaged) ? (speed>50.0 ? (distance<=35.0 ? 5: 10) : 15) : 0;
	}

	public int getPulseCount() {
		return pulseCount;
	}

	public void setPulseCount(int timer) {
		this.pulseCount = timer;
	}

	public boolean isEmerBrake() {
		return emerBrake;
	}

	public void setAutoDisengage(boolean autoDisengage) {
		this.emerBrake = autoDisengage;
	}
}