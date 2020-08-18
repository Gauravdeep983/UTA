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
public class Problem2ClassTest {

	private Problem2Class prb2;
	
	@Before
	public void setUp () {
		prb2 = new Problem2Class();
	}
	
	@Test
	@FileParameters("src/Homework5/Problem2TestCases.csv")	
	public void test(int testcaseNumber, int boxInCarNum, int rrCarNum, int shipmentNum, int boxSum) {		
		assertEquals(boxSum, prb2.calcPrevBoxNumber(boxInCarNum, rrCarNum, shipmentNum));
	}
}