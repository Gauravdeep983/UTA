package Homework5;

public class Problem4Class {

		public double calcCart (double cart, boolean loyaltyCard, boolean validCode, boolean validDigitalCoupon) {
			
		double discount;
		
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

		return ((!validCode && !validDigitalCoupon) || !loyaltyCard) ? (cart * 1.0825) : (cart * (1-discount) * 1.0825);
		}
	}