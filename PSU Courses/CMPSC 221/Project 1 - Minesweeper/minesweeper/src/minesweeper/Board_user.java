/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package minesweeper;

import java.util.ArrayList;

/**
 *
 * @author xvr5040
 */
public class Board_user extends Board {

    private String[][] ub;
    private Board_mine mine;
    ArrayList checked = new ArrayList<>();
    ArrayList flaged = new ArrayList<>();
    private int sqr = 0;
    
    /**
     *
     * @param i, row of the user board
     * @param j, column of the user board
     */
    public Board_user(int i, int j) {
        super(i, j);
        this.setName("User Board");
        this.ub = new String[this.row][this.column];
        this.mine = new Board_mine(this.row, this.column);
        this.mine.fill_board();
        //System.out.println(this.mine.toString());
        for (int a = 0; a < this.row; a++) {
            for (int b = 0; b < this.column; b++) {
                this.ub[a][b] = "[ ]";
            }
        }
    }

    /**
     *
     * @param xy
     */
    //check the numbers around and present them
    public void checkAround(String xy) {
        //convert string to coordinate (int)
        int x = Integer.valueOf(xy.split(",")[0]);
        int y = Integer.valueOf(xy.split(",")[1]);
        ArrayList checking = new ArrayList<>();
        //wether the point was already checked
        if (!checked.contains(Integer.toString(x) + "," + Integer.toString(y))) {
            if (x >= 1 && y >= 1 && x <= this.row && y <= this.column) {
                //synchronize the data from mineBoard
                this.ub[x - 1][y - 1] = this.mine.getMineBoard()[x][y];
                //prevent checking the same point for multiple times
                checked.add(Integer.toString(x) + "," + Integer.toString(y));
                if (" . ".equals(this.mine.getMineBoard()[x][y])) {
                    //the point will be checked later
                    checking.add(Integer.toString(x - 1) + "," + Integer.toString(y - 1));
                    checking.add(Integer.toString(x - 1) + "," + Integer.toString(y));
                    checking.add(Integer.toString(x - 1) + "," + Integer.toString(y + 1));
                    checking.add(Integer.toString(x) + "," + Integer.toString(y - 1));
                    checking.add(Integer.toString(x) + "," + Integer.toString(y + 1));
                    checking.add(Integer.toString(x + 1) + "," + Integer.toString(y - 1));
                    checking.add(Integer.toString(x + 1) + "," + Integer.toString(y));
                    checking.add(Integer.toString(x + 1) + "," + Integer.toString(y + 1));
                    for (Object data : checking) {

                        //loop
                        checkAround((String) data);
                    }
                }
            }
        }
    }

    /**
     *
     * @param x, find through the row
     * @param y, find through the column
     * @return, return if it's a mine or not
     */
    //check if the index you selected is a mine
    public boolean sweep(int x, int y) {
        this.sqr++;
        boolean success = false;
        if (" * ".equals(this.mine.getMineBoard()[x][y])) {
            System.out.println("Sorry, you hit the mine.\nGame Over!");
            //System.out.println(this.mine.toString());
        } else {
            success = true;
            checkAround(Integer.toString(x) + "," + Integer.toString(y));
            // this.ub[x-1][y-1] = this.mine.getMineBoard()[x][y];
        }
        return success;
    }

    /**
     *
     * @param x
     * @param y
     */
    public void flag(int x, int y) {
        this.ub[x - 1][y - 1] = " F ";
        this.flaged.add(x + "," + y);
    }

    /**
     *
     * @param sqr
     * @return
     */
    public boolean checksqr() {
        return this.sqr != (this.row * this.column - this.mine.num_mine);
    }

    public boolean checkflag(){
        int count = 0;

        for (Object i : this.flaged) {
            int x = Integer.valueOf(((String) i).split(",")[0]);
            int y = Integer.valueOf(((String) i).split(",")[1]);
            if (" * ".equals(this.mine.getMineBoard()[x][y])) {
                count++;
            }
        }
        return count == this.mine.num_mine;
    }
    
    /**
     *
     * @return, if mine board is instance of Board class
     */
    public boolean is_inst() {
        return this.mine instanceof Board_mine;
    }

    //print the data inside user board
    @Override
    public String toString() {
        String str = "";
        for (String[] row : this.ub) {
            for (String column : row) {
                str += column;
                str += " ";
            }
            str += "\n";
        }
        return "Board name: User Board\n\n" + str;
    }
    
    /**
     *
     * @return
     */
    public String Fail(){
        return this.mine.toString();
    }
}
