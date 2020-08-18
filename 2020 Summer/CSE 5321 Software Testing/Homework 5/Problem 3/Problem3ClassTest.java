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
public class Problem3ClassTest {

	private Problem3ClassCorrected prb3;
	
	@Before
	public void setUp () {
		prb3 = new Problem3ClassCorrected();
	}
	
	@Test
	@FileParameters("src/Homework5/Problem3TestCases.csv")	
	public void test(int testcaseNumber, Problem3ClassCorrected.state curState, Problem3ClassCorrected.state nextState, int D, int G, int P, int Z, int B, int I, int T, int X) {		
		prb3.operateBinoculars(curState, D, G, P, Z);
		assertEquals(nextState, prb3.getNextState());
		assertEquals(B, prb3.getB());
		assertEquals(I, prb3.getI());
		assertEquals(T, prb3.getT());
		assertEquals(X, prb3.getX());
		
	}
}