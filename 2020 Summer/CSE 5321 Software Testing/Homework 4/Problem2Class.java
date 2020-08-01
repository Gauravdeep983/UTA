package Homework4;

public class Problem2Class {

	public void calcLights (double batteryLevel,Problem2ClassAlarm alarm) {
		boolean red [] = {		false, 	false, 	false, 	false, 	true, 	true};
		boolean yellow [] = {	false, 	false, 	false, 	true, 	true, 	true};
		boolean green [] = {	false, 	false, 	true, 	true, 	true, 	true};
		boolean strobe [] = {	false, 	false, 	false, 	false, 	true, 	false};
		boolean bell [] = {		true, 	true, 	true, 	true, 	false, 	true};
		int index;

		
		if (batteryLevel < 0.1)
			index = 5; 
		else
			if (batteryLevel <= 35.1)
				index = 4;
			else
				if (batteryLevel <= 60.0)
					index = 3;
				else
					if (batteryLevel < 99.8)
						index = 2;
					else
						if (batteryLevel < 100.0)
							index = 1;
						else
							if (batteryLevel < 200.2)
								index = 5;
							else
								index = 0;

		alarm.setRedLight(red[index]);
		alarm.setYellowLight(yellow[index]);
		alarm.setGreenLight(green[index]);
		alarm.setStrobe(strobe[index]);
		alarm.setBell(bell[index]);
	}	
}