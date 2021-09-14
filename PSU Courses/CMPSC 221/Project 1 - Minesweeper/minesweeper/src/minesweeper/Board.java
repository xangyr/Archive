/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package minesweeper;
/**
 *
 * @author xvr5040
 */
public abstract class Board {

    protected int row;
    protected int column;
    protected String name;

    /**
     *
     * @param i, for the size of row
     * @param j, for the size of column
     */
    public Board(int i, int j) {
        this.row = i;
        this.column = j;

    }

    /**
     *
     * @param name, set the name of the board
     */
    public void setName(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return "Board name: " + name;
    }
}
/**
 * public void create_mine() {

        Mine = new Board_mine(height, width);
        Mine.fill_board();
        System.out.print(Mine.toString());

    }

    public void checkAround(String xy) {

        //convert string to coordinate (int)
        int x = Integer.valueOf(xy.split(",")[0]);
        int y = Integer.valueOf(xy.split(",")[1]);
        ArrayList checking = new ArrayList<>();
        //wether the point was already checked
        if (!checked.contains(Integer.toString(x) + "," + Integer.toString(y))) {
            if (x >= 1 && y >= 1 && x <= height && y <= width) {
                //synchronize the data from mineBoard
                buttons[x - 1][y - 1].setText(Mine.getMineBoard()[x][y]);
                
                //prevent checking the same point for multiple times
                checked.add(Integer.toString(x) + "," + Integer.toString(y));
                if (" . ".equals(Mine.getMineBoard()[x][y])) {
                    //the point will be checked later
                    buttons[x - 1][y - 1].setEnabled(false);
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
        frame.pack();
    }
 */