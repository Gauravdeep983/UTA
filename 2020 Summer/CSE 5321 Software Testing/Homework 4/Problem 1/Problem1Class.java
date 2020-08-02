package Homework4;

public class Problem1Class {

	public enum motorStates {Off,RB1,RB2,RB3,RB4,RB5}
	public enum chuteStates {Off,Deployed,Released}
	private motorStates ms; chuteStates cs;
	
	public void controlLanding (double AGL) {
		final motorStates [] motorStatesTab = 	{motorStates.Off,motorStates.RB5,motorStates.RB4,motorStates.RB3,
				 motorStates.RB2,motorStates.RB2,motorStates.RB1,motorStates.Off,};
		final chuteStates [] chuteStatesTab = 	{chuteStates.Off,chuteStates.Off,chuteStates.Off,chuteStates.Off,
				 chuteStates.Deployed,chuteStates.Released,chuteStates.Released,chuteStates.Released};

		int index;
		if (AGL > 7_500.1)
			index = 0;
		else
			if (AGL > 4_100.1)
				index = 1;
			else
				if (AGL >= 2_250.1)
					index = 2;
				else
					if (AGL > 1_100.1)
						index = 3;
					else
						if (AGL > 400.1)
							index = 4;
						else
							if (AGL >= 250.1)
								index = 5;
							else
								if (AGL > 0.0)
									index = 6;
								else
									index = 7;	
		ms = motorStatesTab[index];
		cs = chuteStatesTab[index];
	}

	public motorStates getMs() {
		return ms;
	}

	public void setMs(motorStates ms) {
		this.ms = ms;
	}

	public chuteStates getCs() {
		return cs;
	}

	public void setCs(chuteStates cs) {
		this.cs = cs;
	}
}