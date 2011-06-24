package submission1_2;

import java.util.Scanner;

public class DayOfTheWeek {

    public static void main(String[] args) {
        // Create a new Scanner object to read the input Stream
        Scanner inputScanner = new Scanner(System.in);
        
        // Define some variables
        int date[] = new int[3];        // An array of 3 fields, day/month/year
        String days[] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thirsday", "Friday", "Saturday"};
        int day;
        
        //-- Start the program here,
        // Prompt the user for a date
        System.out.print("Enter a date : ");
        for (int i = 0; i < 3; i++) {
            date[i] = inputScanner.nextInt();
        }
        
        // Using the Zeller's congruence : http://en.wikipedia.org/wiki/Zeller's_congruence
        // Where,
        // date[0] = day
        // date[1] = month
        // date[2] = year
        
        // If the month is Januar or Februar then you count them as the 13th and 14th month of the previous year
        if (date[1] < 3) {
            date[1] += 12;
            date[2] -= 1;
        }

        // Here is the Zeller's congruence formulae
        day = (date[0] + (2 * date[1]) + (6 * (date[1] + 1) / 10) + date[2] + (date[2] / 4) - (date[2] / 100) + (date[2] / 400) + 1) % 7;
        
        // Print some output,
        System.out.printf("%d %d %d falls/fell on a %s", date[0], date[1], date[2], days[day]);
    }

}
