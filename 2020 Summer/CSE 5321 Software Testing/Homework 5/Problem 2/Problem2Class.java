package Homework5;

public class Problem2Class {

	public int calcPrevBoxNumber (int boxInCarNum, int rrCarNum, int shipmentNum) {
		int BoxesperRRCars[] = { 380, 400, 420, 430, 380, 400, 430, 420, 380};
		int boxSum=0;
		if ((shipmentNum % 5 != 0) || ((shipmentNum % 25 != 0) && (shipmentNum % 10 == 0))) 
			{
			BoxesperRRCars[1] = 420;
			BoxesperRRCars[2] = 400;
			}
		
		if ((boxInCarNum==1) && (rrCarNum==1))
			boxSum=4_000;
		else {
			for (int i=0;i<rrCarNum-1;i++)
				boxSum+=BoxesperRRCars[i];
			boxSum+=boxInCarNum-1;
		}
		return boxSum;
	}
}