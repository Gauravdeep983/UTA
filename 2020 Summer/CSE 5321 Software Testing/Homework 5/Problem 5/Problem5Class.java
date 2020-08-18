package Homework5;

public class Problem5Class {

		public double calcCart (Problem5ServerData data, boolean loyaltyCard, boolean validCode, boolean validDigitalCoupon) {
			
		double discount=0,cart;
		cart=data.getCart();
		
		if ((validCode || validDigitalCoupon) && loyaltyCard) {
			if (cart <= 850.0)
				discount = 0.0;
			else
				if (cart < 1_000.0)
					discount = 0.05;
				else
					if (cart <= 1_250.0)
						discount = 0.10;
					else
						if (cart < 1_500.0)
							discount = 0.15;
						else
							if (cart <= 2_500.0)
								discount = 0.2;
							else
								discount = 0.25;
		}
		return  (cart * (1-discount) * 1.0825);
	}
}