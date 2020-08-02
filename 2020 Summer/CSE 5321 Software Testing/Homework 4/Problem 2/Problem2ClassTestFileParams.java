package Homework4;
import static org.junit.Assert.*;

import junitparams.FileParameters;
import junitparams.JUnitParamsRunner;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

@RunWith(JUnitParamsRunner.class)
public class Problem2ClassTestFileParams {

	private Problem2Class prb2;
	private Problem2ClassAlarm prb2Alarm;
	
	@Before
	public void setUp () {
		prb2 = new Problem2Class();
		prb2Alarm = new Problem2ClassAlarm();
	}
	
	@Test
	@FileParameters("src/Homework4/Problem2TestCaseTable11.csv")
	public void test(int testcaseNumber, double batteryLevel, boolean redLight, boolean yellowLight, boolean greenLight, boolean strobe, boolean bell, String bpNumber) {
		prb2.calcLights(batteryLevel, prb2Alarm);
		assertEquals(redLight, prb2Alarm.isRedLight());
		assertEquals(yellowLight, prb2Alarm.isYellowLight());
		assertEquals(greenLight, prb2Alarm.isGreenLight());
		assertEquals(strobe, prb2Alarm.isStrobe());
		assertEquals(bell, prb2Alarm.isBell());
	}
}
