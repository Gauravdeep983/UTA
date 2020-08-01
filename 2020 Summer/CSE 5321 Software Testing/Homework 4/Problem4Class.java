package Homework4;

public class Problem4Class {

	public enum autoClaveEnum {NoSterilization, SomeSterilized, PartialSterilized, FullySterilized};

	public Problem4Class.autoClaveEnum autoClave (boolean autoclaveOn, double temperature, double pressure) {

		autoClaveEnum action=Problem4Class.autoClaveEnum.NoSterilization;
		if (autoclaveOn) 
			if (temperature > 212.0) {
				if (pressure >= 3_500.0)
					if (pressure < 5_000.0)
						action = Problem4Class.autoClaveEnum.FullySterilized; }
			else {
				if (temperature > 100.0)
					if (pressure > 1_900.0)
						if (pressure < 3_500.0)
							action = Problem4Class.autoClaveEnum.PartialSterilized; }
		else
			action = Problem4Class.autoClaveEnum.SomeSterilized;
		return action;
	}
}