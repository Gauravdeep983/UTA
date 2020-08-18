package Homework5;

import static org.junit.Assert.*;
import static junitparams.JUnitParamsRunner.$;
import static org.junit.Assert.*;
import junitparams.JUnitParamsRunner;
import junitparams.Parameters;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.Before;
import org.junit.Test;

import junitparams.FileParameters;

@RunWith(JUnitParamsRunner.class)
public class Problem4ClassTest {
	
	private Problem4Class prb4;
	
	@Before
	public void setUp() throws Exception {	
		prb4 = new Problem4Class();
	}

	@Test
	@FileParameters("src/Homework5/Problem4TestCases.csv")	
	public void test(int testcaseNumber, double cart, boolean loyaltyCard, boolean validCode, boolean validDigitalCoupon, double output, String BasisPath, String MCDC ) {
		prb4.calcCart(cart, loyaltyCard, validCode, validDigitalCoupon);
		assertEquals(output, prb4.calcCart(cart, loyaltyCard, validCode, validDigitalCoupon),0.01);
	}

}
