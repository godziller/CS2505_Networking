import java.util.Scanner;

public class ThreeDArraySearch {
	public static void main(String[] args){
	
		//Create 3D array with sample values
		int[][][] threeDArray = {
			{
                		{1, 2, 3},
                		{4, 5, 6}
            		},
            		{
                		{7, 8, 9},
                		{10, 11, 12}
            		},
            		{
                		{13, 14, 15},
                		{16, 17, 18}
            		}

		};

		// Display the 3d Array: 
		System.out.println("2D Array Contents: ");
		for (int i = 0; i < threeDArray.length; i++){
		
			for (int j = 0; j < threeDArray[i].length; j++ ){
			
				for (int k = 0; k < threeDArray[i][j].length; k++){
					System.out.println(threeDArray[i][j][k]);
				}
			}
			System.out.println();
		}

		// Create scanner object
		Scanner scanner = new Scanner(System.in);
		System.out.println("Enter a number you want to search for in the array: ");
		int numberToFind = scanner.nextInt();	// Store next int for use
		scanner.close();	// close scanner for hygiene

		// bool to set found condition -> found if in 3dArray.
		boolean found = false;
		for (int i = 0; i < threeDArray.length; i++){
			for (int j = 0; j < threeDArray[i].length; j++){
				for (int k = 0; k < threeDArray[i][j].length; k++){
					if (threeDArray[i][j][k] == numberToFind){
						// Set bool and print.
						found = true;
						System.out.println("Number " + numberToFind + " found in position: ["+i+"]["+j+"]["+k+"]");
					}
				}
			}
		}

		// If the number entered is Not in the 3dArray: 
		if (!found) {
			System.out.println("Number was not found in the 3d Array");
		}
	}
}
