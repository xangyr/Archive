package minesweeper;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
import java.util.Scanner;

/**
 *
 * @author xvr5040
 */
public class Minesweeper {

    int[] max_size = new int[2];                        //set an array to store the size of the board, in case user won't input larger row or column
    static Board_user u_b;                              //define user board, so can use this()

    /**
     *
     * @return, display the level menu
     */
    public String choose_lvl() {                        //menu choosing level
        Scanner input = new Scanner(System.in);
        System.out.println("*******************\nSelect difficulty:\n\t1. Easy\n\t2. Medium\n\t3. Expert\n\t4. Customized\n*******************");

        return input.next();
    }

    /**
     *
     * @param i, size of row
     * @param j, size of column
     */
    public void build_board(int i, int j) { // for user only
        Minesweeper.u_b = new Board_user(i, j);
    }

    /**
     *
     * @return the coordinate of the sqr that user choose
     */
    public String[] choose_sqr() {
        Scanner input = new Scanner(System.in);
        System.out.println("Choose the square you want to deal with, and input in such format: row,column");    //let user choose the square, having a format
        String line = input.nextLine();
        Integer sqr_r = Integer.valueOf(line.split(",")[0]);
        Integer sqr_c = Integer.valueOf(line.split(",")[1]);
        while (sqr_r > this.max_size[0] || sqr_c > this.max_size[1]) {                                          //if the square isn't in the board, input again
            System.out.println("Please input number smaller or equal to the size of your board");
            line = input.nextLine();
            sqr_r = Integer.valueOf(line.split(",")[0]);
            sqr_c = Integer.valueOf(line.split(",")[1]);
        }
        return line.split(",");
    }

    /**
     *
     *
     * @return whether user hit the mine
     */
    public boolean play() {
        Scanner input = new Scanner(System.in);
        String[] line = choose_sqr();                                                                           //let user choose square first, then will display the whole userboard if the square isn't mine

        boolean b = true;                                                                                       //set b to true, if sweep a mine, then it will be false and the game will stop

        int sqr_r = Integer.valueOf(line[0]);
        int sqr_c = Integer.valueOf(line[1]);
        System.out.println("Choose the following methods:\n\t1. Sweep it\n\t2. Flag it");                       //choose what to do to the square
        String choose = input.next();
        if ("1".equals(choose)) {
            b = Minesweeper.u_b.sweep(sqr_r, sqr_c);

        } else if ("2".equals(choose)) {
            Minesweeper.u_b.flag(sqr_r, sqr_c);
        }
        return b;
    }

    /**
     *
     */
    public void menu() {   //menu for user
        Scanner input = new Scanner(System.in);
        System.out.println("Welcome to this game!\nGet ready to play.");
        System.out.println("*******************");
        System.out.println("User Menu:\n\t1. Play a new round\n\t2. Continue last board\n\t3. Tell me about the Rules\n\t4. exit\n*******************");         //choose level
        String choose = input.next();                                                                                                                           //then build the board
        if ("1".equals(choose)) {
            String level = choose_lvl();
            if ("1".equals(level)) {
                build_board(9, 9);
                this.max_size[0] = 9;
                this.max_size[1] = 9;
            } else if ("2".equals(level)) {
                build_board(16, 16);
                this.max_size[0] = 16;
                this.max_size[1] = 16;
            } else if ("3".equals(level)) {
                build_board(16, 30);
                this.max_size[0] = 16;
                this.max_size[1] = 30;
            } else if ("4".equals(level)) {
                System.out.println("Input the size of the board (9*9 to 30*24)\nRow: ");
                int cus_r = input.nextInt();
                System.out.print("Column: ");
                int cus_c = input.nextInt();
                build_board(cus_r, cus_c);
                this.max_size[0] = cus_r;
                this.max_size[1] = cus_c;
            }
        } 
        
        // TODO create a file store the unfinished board in it
        else if ("2".equals(choose)) {
            System.out.println("Sorry, we are still working on that feature\nStarting a new board");
            String level = choose_lvl();
            if ("1".equals(level)) {
                build_board(9, 9);
                this.max_size[0] = 9;
                this.max_size[1] = 9;
            } else if ("2".equals(level)) {
                build_board(16, 16);
                this.max_size[0] = 16;
                this.max_size[1] = 16;
            } else if ("3".equals(level)) {
                build_board(16, 30);
                this.max_size[0] = 16;
                this.max_size[1] = 30;
            } else if ("4".equals(level)) {
                System.out.print("Input the size of the board (9*9 to 30*24)\nRow: ");
                int cus_r = input.nextInt();
                System.out.print("Column: ");
                int cus_c = input.nextInt();
                build_board(cus_r, cus_c);
                this.max_size[0] = cus_r;
                this.max_size[1] = cus_c;
            }
        } else if ("3".equals(choose)) {
            System.out.println(this.toString());
            menu();
        } else if ("4".equals(choose)) {
            System.out.println("Thank you! Goodbye!");  //if choose exit, exit the program
            System.exit(0);
        }
    }

    @Override
    public String toString() {                      // this is the rule
        return "Rules:\n\t1. '.' used to present the blank space\n\t   '*' used to present the mine\n\t   Digits represent the # of mines around\n\t   'F' used to present the flaged square\n\t2. You can flag every square\n\t3. Only sweep the square that is not mine, if you hit the mine then the game is over\n\t4. 10 mines for EASY, 40 mines for MEDIUM, and 99 mines for EXPERT";
    }

    
    /*public static void main(String[] args) {
        boolean not_mine;    //use while true to run the program
        String choice;

        do {
            Scanner in = new Scanner(System.in);
            not_mine = true;
            int sqr_rvl = 0;                                //how many squares are revealed

            Minesweeper game = new Minesweeper();
            game.menu();

            do {
                System.out.println(Minesweeper.u_b.toString());
                not_mine = game.play();                                                //return true of false when sweep, true for isn't mine, false for hit the mine and fail
                sqr_rvl++;
            } while (not_mine && Minesweeper.u_b.checksqr() && !Minesweeper.u_b.checkflag());    //if the user hit the mine, or they reveal all squares, or they flag all mines, stop the program

            System.out.println(Minesweeper.u_b.Fail());

            //after choose x and y, if sweep a mine return false, print line below
            System.out.println("Would you like to play another round?\nEnter \"Y\" or \"y\" for yes\t");    //ask for another round
            choice = in.nextLine();
        } while ("Y".equals(choice.toUpperCase()));

    }*/

}
