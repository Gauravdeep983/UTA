package Homework5;
import static junitparams.JUnitParamsRunner.$;
import static org.junit.Assert.*;
import org.easymock.EasyMock;
import junitparams.FileParameters;
import junitparams.JUnitParamsRunner;
import junitparams.Parameters;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

@RunWith(JUnitParamsRunner.class)
public class Problem5ClassTest {

	private Problem5Class prb5;
	Problem5ServerData mockObject;
	
	@Before
	public void setUp() {
		prb5 = new Problem5Class();
		mockObject =  EasyMock.strictMock(Problem5ServerData.class);
	}
	
	@Test
	@FileParameters("src/Homework5/Problem5TestCases.csv")	
	public void test(int testcaseNumber, double cart, boolean loyaltyCard, boolean validCode, boolean validDigitalCoupon, double output, String basisPath, String MCDC) {		
		EasyMock.expect(mockObject.getCart()).andReturn(cart);
		EasyMock.replay(mockObject);
		assertEquals(output,prb5.calcCart(mockObject, loyaltyCard, validCode, validDigitalCoupon),0.01);
	}
}