package Homework4;
import static junitparams.JUnitParamsRunner.$;
import static org.junit.Assert.*;
import junitparams.FileParameters;
import junitparams.JUnitParamsRunner;
import junitparams.Parameters;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

import Homework4.Problem4Class.autoClaveEnum;

@RunWith(JUnitParamsRunner.class)
public class Problem4ClassTestFileParams {

	private Problem4Class prb4;
	
	@Before
	public void setUp () {
		prb4 = new Problem4Class();
	}
	
	@Test
	@FileParameters("src/Homework4/Problem4TestCaseTable.csv")	
	public void test(int testcaseNumber, boolean autoclaveOn, double temperature, double pressure, Problem4Class.autoClaveEnum returnVal, String bpNumber, String comments) {		
		//prb4.autoClave(autoclaveOn, temperature, pressure);
		assertEquals(returnVal, prb4.autoClave(autoclaveOn, temperature, pressure));
	}
}