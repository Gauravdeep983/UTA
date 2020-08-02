package Homework4;

import static junitparams.JUnitParamsRunner.$;
import static org.junit.Assert.*;
import junitparams.FileParameters;
import junitparams.JUnitParamsRunner;
import junitparams.Parameters;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

@RunWith(JUnitParamsRunner.class)
public class Problem5ClassTestFileParams {

	private Problem5Class prb5;
	
	@Before
	public void setUp () {
		prb5 = new Problem5Class();
	}
	
	@Test
	@FileParameters("src/Homework4/Problem5TestCaseTable.csv")	
	public void test(int testcaseNumber, double x, double y, String bpNumber) {
		assertEquals(y, prb5.calcY(x), 0.001);
	}
}