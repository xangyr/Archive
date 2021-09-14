/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package minesweeper;

/**
 *
 * @author zfx5036
 */
import java.util.Random;

public class Board_mine extends Board {

    private String mine[][];
    int num_mine;
    /**
     *
     * @param i, row of the board, but to count the # of mines, i += 2
     * @param j, column of the board, to count, j += 2
     */
    public Board_mine(int i, int j) {
        super(i, j);
        this.setName("Mines board");
        //two more row and column, in order to count the # of mines later
        this.mine = new String[this.row + 2][this.column + 2];
        for (int r = 0; r < this.row + 2; r++) {
            for (int c = 0; c < this.column + 2; c++) {
                this.mine[r][c] = "";
            }
        }
        Random rand = new Random();
        
        // the number of mines of stored board
        if (this.row == 9 && this.column == 9) {
            this.num_mine = 10;
        } else if (this.row == 16 && this.column == 16) {
            this.num_mine = 40;
        } else if (this.row == 16 && this.column == 30) {
            this.num_mine = 99;

            //the # of mines of customized board
        } else {
            this.num_mine = rand.nextInt((this.row - 1) * (this.column - 1)) + 1;
        }
        // store mines in board
        for (int iMine = 0; iMine < this.num_mine; iMine++) {
            int MineRow = rand.nextInt(this.row) + 1;
            int MineColumn = rand.nextInt(this.column) + 1;
            //prevent conflict
            while (" * ".equals(this.mine[MineRow][MineColumn])) {
                MineRow = rand.nextInt(this.row) + 1;
                MineColumn = rand.nextInt(this.column) + 1;
            }
            this.mine[MineRow][MineColumn] = " * ";
        }
    }

    //fill the empty space in the mine board with the number of mines around
    public void fill_board() {

        for (int r = 1; r < this.row + 1; r++) {
            for (int c = 1; c < this.column + 1; c++) {

                String str = "";
                //add the space around and count the length of it
                if ("".equals(this.mine[r][c])) {
                    str = this.mine[r - 1][c - 1] + this.mine[r][c - 1] + this.mine[r + 1][c - 1] + this.mine[r - 1][c] + this.mine[r + 1][c] + this.mine[r - 1][c + 1] + this.mine[r][c + 1] + this.mine[r + 1][c + 1];

                    if (str.contains(" * ")) {
                        this.mine[r][c] = "" + Integer.toString(str.length() - str.replace("*", "").length()) + "";

                    } else {
                        this.mine[r][c] = " . ";
                    }
                }
            }
        }
    }

    /**
     *
     * @return, mine board to Board 2 class
     */
    public String[][] getMineBoard() {
        return this.mine;
    }

    //print the data inside the mine board
    @Override
    public String toString() {
        String str = "";
        for (String[] row : this.mine) {
            for (String column : row) {
                str += column;
                str += " ";
            }
            str += "\n";
        }
        return "Board name: Mine Board\n\n" + str;
    }

}
