package Homework4;

public class Problem3Class {

	public boolean approveCart (boolean prime, int memberPoints, double total) {
		   boolean purchase=false;

		   if (prime) {
			   if (memberPoints > 1_000)
				   purchase = true;
			   else
				   if (total <= 6_500.0)
					   if (total > 2_500.0)
						   purchase = true; }
		   else {
			   if (memberPoints >= 551)
				   if (total < 9_000.0)
					   if (total > 6_500.0)
						   purchase = true; }
		   return purchase;
		}
}