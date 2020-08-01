package Homework4;

public class Problem5Class {
	private double y;
	
	public double calcY (double x) {

		if (x < -1.0)
			y=6.0;
		else
			if (x < 0.0)
				y=7.0;
			else
				if (x <= 2.0)
					y=7-3.5*x;
				else
					if (x <= 6.0)
						y=-(x-4.0)*(x-4.0)+4.0;
					else
						if (x <= 8.0)
							y=3.0*x-18.0;
						else
							if(x <= 9.0)
								y=6.0;
							else
								y=7.0;
		return y;
	}

	public void setY(double y) {
		this.y = y;
	}
}
