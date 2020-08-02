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
public class Problem3ClassTestFileParams {

	private Problem3Class prb3;
	
	@Before
	public void setUp () {
		prb3 = new Problem3Class();
	}
	
	@Test
	@FileParameters("src/Homework4/Problem3TestCaseTable.csv")	
	public void test(int testcaseNumber, boolean prime, int memberPoints, double total, boolean output, String bpNumber) {		
		//prb3.approveCart(prime, memberPoints, total);
		assertEquals(output, prb3.approveCart(prime, memberPoints, total));
	}
}