package Homework4;
import static junitparams.JUnitParamsRunner.$;
import static org.junit.Assert.*;
import junitparams.JUnitParamsRunner;
import junitparams.Parameters;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

import Homework4.Problem1Class.chuteStates;
import Homework4.Problem1Class.motorStates;

@RunWith(JUnitParamsRunner.class)
public class Problem1ClassTestJUnitParams {

	private Problem1Class prb1;
	
	@SuppressWarnings("unused")
	private static final Object[] parametersForProblem1ClassTest () {
		return $(
//				Parameters are: (1,2,3)
//								1=AGL, 2=motorState, 3=chuteState
//				Test case 1
				$(7_500.2,   motorStates.Off,	chuteStates.Off),
//				Test case 2
				$(4_100.2,   motorStates.RB5,	chuteStates.Off),
//				Test case 3
				$(2_250.1,   motorStates.RB4,	chuteStates.Off),
//				Test case 4
				$(1_100.2,   motorStates.RB3,	chuteStates.Off),
//				Test case 5
				$(400.2,   motorStates.RB2,	chuteStates.Deployed),
//				Test case 6
				$(250.1,   motorStates.RB2,	chuteStates.Released),
//				Test case 7
				$(0.1,   motorStates.RB1,	chuteStates.Released),
//				Test case 8
				$(0.0,   motorStates.Off,	chuteStates.Released),
//				Test case 9
				$(250.0,   motorStates.RB1,	chuteStates.Released),
//				Test case 10
				$(400.1,   motorStates.RB2,	chuteStates.Released),
//				Test case 11
				$(1_100.1,   motorStates.RB2,	chuteStates.Deployed),
//				Test case 12
				$(2_250.0,  motorStates.RB3,	chuteStates.Off),
//				Test case 13
				$(4_100.1,    motorStates.RB4,	chuteStates.Off),
//				Test case 14
				$(7_500.1,   motorStates.RB5,	chuteStates.Off),
//				Test case 15
				$(10_000.0,   motorStates.Off,	chuteStates.Off)
				
		);
	}

	@Before
	public void setUp () {
		prb1 = new Problem1Class();
	}
	
	@Test
	@Parameters(method="parametersForProblem1ClassTest")
	public void test(double AGL, Problem1Class.motorStates expMS, Problem1Class.chuteStates expCS) {
		prb1.controlLanding(AGL);
		assertEquals(expMS, prb1.getMs());
		assertEquals(expCS, prb1.getCs());		
	}
}
