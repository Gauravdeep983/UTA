package Homework4;

public class Problem6Class {

	public int determineEdge (boolean a, boolean b, boolean c, boolean d) {
		return (a&&b&&c) ? (d ? 2:1) : (!a ? (c ? 5:4):3);
	}
}
