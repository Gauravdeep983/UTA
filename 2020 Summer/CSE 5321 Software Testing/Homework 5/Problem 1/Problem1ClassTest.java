package Homework5;
import static junitparams.JUnitParamsRunner.$;
import static org.junit.Assert.*;

import junitparams.FileParameters;
import junitparams.JUnitParamsRunner;
import junitparams.Parameters;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

@RunWith(JUnitParamsRunner.class)
public class Problem1ClassTest {

	private Problem1Class prb1;
	
	@Before
	public void setUp () {
		prb1 = new Problem1Class();
	}
	
	@Test
	@FileParameters("src/Homework5/Problem1TestCases.csv")	
	public void test(int testcaseNumber, boolean cruiseEngaged, double speed, double distance, boolean emerBrake, int pulseCount, String MCDC) {		
		prb1.emerBrakeFunction(cruiseEngaged, speed, distance);
		assertEquals(emerBrake, prb1.isEmerBrake());
		assertEquals(pulseCount, prb1.getPulseCount());
	}
}