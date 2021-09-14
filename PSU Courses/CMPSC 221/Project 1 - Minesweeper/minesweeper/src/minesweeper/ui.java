/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package minesweeper;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.util.ArrayList;
import javax.swing.*;

/**
 *
 * @author rj & hang
 */
public class ui implements ActionListener, MouseListener, KeyListener, ItemListener {

    JFrame frame = new JFrame("Minesweeper");
    JPanel panel = new JPanel();
    JButton[][] buttons;
    int height;
    int width;
    Icon flag = new ImageIcon(Toolkit.getDefaultToolkit().getImage("icon/flag.png"));
    Icon mine = new ImageIcon(Toolkit.getDefaultToolkit().getImage("icon/mine.png"));
    private Board_mine Mine;
    private boolean lose;
    private ArrayList checked;
    private int flagged_mine;
    private int revealed_sqr;
    private boolean left_press = false;
    private boolean right_press = false;
    private final Dimension dimension = Toolkit.getDefaultToolkit().getScreenSize();

    //components for main ui window
    private JMenuItem About;
    private JCheckBoxMenuItem Customized;
    private ButtonGroup Difficulty;
    private JCheckBoxMenuItem Easy;
    private JMenuItem Exit;
    private JCheckBoxMenuItem Expert;
    private JMenu Game;
    private JMenu Help;
    private JCheckBoxMenuItem Medium;
    private JMenuBar Menu;
    private JMenuItem New_game;
    private JMenuItem Rules;
    private JPopupMenu.Separator jSeparator1;
    private JPopupMenu.Separator jSeparator2;

    //components for popup customized window
    JFrame cus;
    JPanel p;
    JLabel w;
    JLabel h;
    JTextField txt_w;
    JTextField txt_h;
    JButton create;

    public ui() {
        initComponents();

        frame.setContentPane(panel);

        //frame.setMinimumSize(new Dimension());
        frame.setVisible(true);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        frame.setLayout(new BorderLayout());
        frame.setResizable(false);
        buttons();

    }

    private void initComponents() {
        Difficulty = new javax.swing.ButtonGroup();
        Menu = new javax.swing.JMenuBar();
        Game = new javax.swing.JMenu();
        New_game = new javax.swing.JMenuItem();
        jSeparator1 = new javax.swing.JPopupMenu.Separator();
        Easy = new javax.swing.JCheckBoxMenuItem();
        Medium = new javax.swing.JCheckBoxMenuItem();
        Expert = new javax.swing.JCheckBoxMenuItem();
        Customized = new javax.swing.JCheckBoxMenuItem();
        jSeparator2 = new javax.swing.JPopupMenu.Separator();
        Exit = new javax.swing.JMenuItem();
        Help = new javax.swing.JMenu();
        Rules = new javax.swing.JMenuItem();
        About = new javax.swing.JMenuItem();

        Game.setText("Game");

        New_game.setAccelerator(javax.swing.KeyStroke.getKeyStroke(java.awt.event.KeyEvent.VK_F2, 0));
        New_game.setText("New game");
        New_game.addActionListener(this);

        Game.add(New_game);
        Game.add(jSeparator1);

        Difficulty.add(Easy);
        Easy.setSelected(true);
        Easy.setText("Easy");
        //Easy.addActionListener(this);
        Easy.addItemListener(this);

        Game.add(Easy);

        Difficulty.add(Medium);
        //Medium.setSelected(true);
        Medium.setText("Medium");
        //Medium.addActionListener(this);
        Medium.addItemListener(this);

        Game.add(Medium);

        Difficulty.add(Expert);
        //Expert.setSelected(true);
        Expert.setText("Expert");
        //Expert.addActionListener(this);
        Expert.addItemListener(this);

        Game.add(Expert);

        Difficulty.add(Customized);
        Customized.setText("Customized");
        //Customized.addActionListener(this);
        Customized.addItemListener(this);
        Customized.setToolTipText("Create a cunstomized board with random number of mines");

        Game.add(Customized);
        Game.add(jSeparator2);

        Exit.setText("Exit");
        Exit.addActionListener(this);

        Game.add(Exit);

        Menu.add(Game);

        Help.setText("Help");

        Rules.setText("Rules");
        Rules.addActionListener(this);

        Help.add(Rules);

        About.setText("About");
        About.addActionListener(this);

        Help.add(About);

        Menu.add(Help);

        frame.setJMenuBar(Menu);

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(frame.getContentPane());
        frame.getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
                layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                        .addGap(0, 262, Short.MAX_VALUE)
        );
        layout.setVerticalGroup(
                layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                        .addGap(0, 278, Short.MAX_VALUE)
        );

        frame.pack();

    }

    public void buttons() {
        if (Easy.isSelected()) {
            height = 9;
            width = 9;
            //frame.setSize(304, 350);
        }
        if (Medium.isSelected()) {
            height = 16;
            width = 16;
            //frame.setSize(528, 574);
        }
        if (Expert.isSelected()) {
            height = 16;
            width = 30;
            //frame.setSize(976, 574);
        }
        panel.setLayout(new GridLayout(height, width));
        buttons = new JButton[height][width];
        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++) {
                buttons[i][j] = new JButton();
                buttons[i][j].setMargin(new Insets(0, 0, 0, 0));
                buttons[i][j].addMouseListener(this);
                panel.add(buttons[i][j]);
            }
        }
        lose = false;
        flagged_mine = 0;
        revealed_sqr = 0;
        left_press = false;
        right_press = false;
        checked = new ArrayList<>();

        create_mine();

        //System.out.println(Mine.num_mine + " " + (height * width - Mine.num_mine));
        frame.pack();
        frame.setSize(width * 32 + 16, height * 32 + 62);
        frame.setLocation((int) (dimension.getWidth() - frame.getWidth()) / 2, (int) (dimension.getHeight() - frame.getHeight()) / 2);
        //System.out.println(Mine.num_mine);
    }

    public void customized() {

        cus = new JFrame("Customize board");
        cus.setVisible(true);
        cus.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        cus.setSize(200, 130);
        cus.setResizable(false);
        p = new JPanel();
        w = new JLabel("Input the Width (9 ~ 30)");
        h = new JLabel("Input the Height (9 ~ 24)");
        create = new JButton("Create board");
        create.addActionListener(this);
        txt_w = new JTextField(2);
        //txt_w.addActionListener(this);
        //txt_w.setEnabled(true);
        txt_h = new JTextField(2);
        //txt_h.addActionListener(this);
        //txt_h.setEnabled(true);
        /*width = 0;
        height = 0;*/
        cus.setLocation(frame.getX() + frame.getWidth() / 2 - cus.getWidth() / 2, frame.getY() + frame.getHeight() / 2 - cus.getHeight() / 2);

        //tell user the number is too big
        /*warn = new JFrame("Warning");
        warn.setVisible(false);
        warn.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        warn.setSize(180, 70);
        warn.setResizable(false);
        warn.add(new JLabel("Please input smaller number"));
        warn.setLocation(frame.getX() + frame.getWidth() / 2 - warn.getWidth() / 2, frame.getY() + frame.getHeight() / 2 - warn.getHeight() / 2);

        OK = new JButton("OK");
        OK.addActionListener(this);
         */
        cus.setContentPane(p);
        p.add(w);
        p.add(txt_w);
        p.add(h);
        p.add(txt_h);
        p.add(create);
    }

    public void create_mine() {

        Mine = new Board_mine(height, width);
        Mine.fill_board();

        //System.out.print(Mine.toString());
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
                if (Mine.getMineBoard()[x][y].equals(" . ")) {
                    buttons[x - 1][y - 1].setText("");
                } else {
                    buttons[x - 1][y - 1].setText(Mine.getMineBoard()[x][y]);
                }
                buttons[x - 1][y - 1].setEnabled(false);
                revealed_sqr += 1;
                //prevent checking the same point for multiple times
                checked.add(Integer.toString(x) + "," + Integer.toString(y));
                if (" . ".equals(Mine.getMineBoard()[x][y])) {
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
        //frame.validate();
        //frame.pack();
        if (revealed_sqr == height * width - Mine.num_mine) {
            win();
        }
    }

    public boolean left_right_condition(int x, int y) {
        int dx = 0;
        int dy = 0;
        int flag_around = 0;
        for (int i = -1; i < 2; i++) {
            for (int j = -1; j < 2; j++) {
                dx = x + i;
                dy = y + j;
                if (dx >= 0 && dy >= 0 && dx < height && dy < width) {
                    if (buttons[dx][dy].getIcon() == flag) {
                        flag_around += 1;
                    }
                }
            }
        }
        //frame.validate();
        //System.out.println(flag_around);
        return flag_around == Integer.valueOf(buttons[x][y].getText());
    }

    public void left_right(int x, int y) {
        int dx = 0;
        int dy = 0;
        for (int i = -1; i < 2; i++) {
            for (int j = -1; j < 2; j++) {
                dx = x + i;
                dy = y + j;
                if (!buttons[x][y].isEnabled()) {
                    if (dx >= 0 && dy >= 0 && dx < height && dy < width) {
                        if (buttons[dx][dy].getIcon() != flag) {
                            if (Mine.getMineBoard()[dx + 1][dy + 1].equals(" * ")) {

                                buttons[dx][dy].setIcon(mine);
                                lose = true;
                                lost();
                            } else {
                                checkAround(Integer.toString(dx + 1) + "," + Integer.toString(dy + 1));
                            }
                            buttons[dx][dy].setEnabled(false);
                        }
                    }

                }
            }
        }
        //frame.validate();
    }

    public void lost() {
        if (lose) {
            for (int x = 0; x < height; x++) {
                for (int y = 0; y < width; y++) {
                    if (Mine.getMineBoard()[x + 1][y + 1].equals(" * ")) {
                        buttons[x][y].setIcon(mine);
                    } else if (Mine.getMineBoard()[x + 1][y + 1].equals(" . ")) {
                        buttons[x][y].setText("");
                    } else {
                        buttons[x][y].setText(Mine.getMineBoard()[x + 1][y + 1]);
                    }
                    buttons[x][y].setEnabled(false);
                }
            }
        }
        //frame.validate();
    }

    public void win() {
        if (!lose) {
            for (int x = 0; x < height; x++) {
                for (int y = 0; y < width; y++) {
                    if (Mine.getMineBoard()[x + 1][y + 1].equals(" * ")) {
                        buttons[x][y].setIcon(mine);
                    } else if (Mine.getMineBoard()[x + 1][y + 1].equals(" . ")) {
                        buttons[x][y].setText("");
                    } else {
                        buttons[x][y].setText(Mine.getMineBoard()[x + 1][y + 1]);
                    }
                    buttons[x][y].setEnabled(false);

                }
            }
            JOptionPane.showMessageDialog(frame, "Congratuation! You win!");
        }
        lose = true;
        //frame.validate();
    }

    public static void main(String[] args) {
        /*try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(ui.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(ui.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(ui.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(ui.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
         */
        new ui();

    }

    @Override
    public void actionPerformed(ActionEvent evt) {
        if (evt.getSource().equals(New_game)) {
            //reset the game
            panel.removeAll();
            if (Customized.isSelected()) {
                customized();
            } else {
                buttons();
            }
        }
        /*if (evt.getSource().equals(Easy) || evt.getSource().equals(Medium) || evt.getSource().equals(Expert)) {
            panel.removeAll();
            buttons();
        }
        if (evt.getSource().equals(Customized) && Customized.isSelected()) {
            panel.removeAll();
            customized();
        }*/
        if (evt.getSource().equals(Exit)) {
            System.exit(0);
        }
        if (evt.getSource().equals(Rules)) {
            JFrame rule = new JFrame("HELP");
            rule.setVisible(true);
            rule.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
            rule.setLayout(new FlowLayout());
            rule.setSize(880, 130);
            rule.setResizable(false);
            rule.setLocation(frame.getX() + frame.getWidth() / 2 - rule.getWidth() / 2, frame.getY() + frame.getHeight() / 2 - rule.getHeight() / 2);
            JPanel p1 = new JPanel();
            JLabel r1 = new JLabel("The goal is to uncover all the squares that do not contain mines and don't blow yourself up.");
            JLabel r2 = new JLabel("The location of the mines is discovered by a process of logic, using patterns and a little guessing.");
            JLabel r3 = new JLabel("Some squares are blank but some contain numbers (1 to 8), each number being the number of mines adjacent to the uncovered square.");
            JLabel r4 = new JLabel("To help avoid hitting a mine, the location of a suspected mine can be marked by flagging it with the right mouse button.");
            rule.setContentPane(p1);
            p1.add(r1);
            p1.add(r2);
            p1.add(r3);
            p1.add(r4);
        }
        if (evt.getSource().equals(About)) {
            JFrame about = new JFrame("ABOUT");
            about.setVisible(true);
            about.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);;
            about.setSize(300, 110);
            about.setResizable(false);

            about.setLocation(frame.getX() + frame.getWidth() / 2 - about.getWidth() / 2, frame.getY() + frame.getHeight() / 2 - about.getHeight() / 2);
            //about.setLayout();

            JPanel p1 = new JPanel();
            //p1.setLayout(new SpringLayout());
            JLabel r1 = new JLabel("@ Minesweeper");
            JLabel r2 = new JLabel("Version 0.11 (Build 3_20-19) || No Copyright");
            JLabel r3 = new JLabel("by Xiangyu Ren and Zihang Xu");
            about.setContentPane(p1);
            p1.add(r1);
            p1.add(r2);
            p1.add(r3);
        }
        if (evt.getSource().equals(create)) {
            width = Integer.valueOf(txt_w.getText());
            height = Integer.valueOf(txt_h.getText());
            if (width < 9 || width > 30 || height < 9 || height > 24) {
                JOptionPane.showMessageDialog(frame, "Please input valid number", "Warning", JOptionPane.WARNING_MESSAGE);
                //Easy.setSelected(true);
            } else {
                buttons();
            }
            cus.dispose();
        }

    }

    @Override
    public void mouseClicked(MouseEvent me) {

        for (int x = 0; x < height; x++) {
            for (int y = 0; y < width; y++) {
                if (me.getSource().equals(buttons[x][y])) {
                    if (me.getButton() == MouseEvent.BUTTON1) {
                        //System.out.println(revealed_sqr);

                        if (buttons[x][y].getIcon() != flag) {
                            while (revealed_sqr == 0 && !Mine.getMineBoard()[x + 1][y + 1].equals(" . ")) {
                                create_mine();
                            }
                            if (Mine.getMineBoard()[x + 1][y + 1].equals(" * ")) {

                                buttons[x][y].setIcon(mine);
                                lose = true;
                                lost();

                            } /*else if (Mine.getMineBoard()[x + 1][y + 1].equals(" . ")) {
                                buttons[x][y].setText("");
                                buttons[x][y]
                            } else {
                                buttons[x][y].setText(Mine.getMineBoard()[x + 1][y + 1]);
                            }*/ else {
                                checkAround(Integer.toString(x + 1) + "," + Integer.toString(y + 1));
                            }

                            /*System.out.println(buttons[x][y].getWidth()+" "+buttons[x][y].getHeight());
                            if (buttons[x][y].getWidth() == 32 && buttons[x][y].getHeight() == 32) {
                                System.out.println(frame.getWidth()+" "+frame.getHeight());
                            }*/
                            buttons[x][y].setEnabled(false);

                            //System.out.println(revealed_sqr);
                        }

                    }
                    if (me.getButton() == MouseEvent.BUTTON3) {
                        if (buttons[x][y].getIcon() == flag) {
                            buttons[x][y].setIcon(null);
                        } else if (buttons[x][y].isEnabled()) {
                            //buttons[x][y].setText("F");
                            //buttons[x][y].setIcon(defaultIcon);
                            buttons[x][y].setIcon(flag);
                        }

                    }

                    if (buttons[x][y].getIcon() == flag && Mine.getMineBoard()[x + 1][y + 1].equals(" * ")) {
                        flagged_mine += 1;
                        if (flagged_mine == Mine.num_mine && revealed_sqr == height * width - Mine.num_mine) {
                            //System.out.println(flagged_mine + " " + Mine.num_mine + " " + revealed_sqr + " " + (height * width - Mine.num_mine));
                            win();
                        }
                    }
                    if (revealed_sqr == height * width - Mine.num_mine) {
                        win();
                    }

                }

            }
        }
    }

    @Override
    public void mousePressed(MouseEvent me) {
        if (me.getButton() == MouseEvent.BUTTON1) {
            left_press = true;
        } else if (me.getButton() == MouseEvent.BUTTON3) {
            right_press = true;
        }
        if (left_press && right_press) {
            for (int x = 0; x < height; x++) {
                for (int y = 0; y < width; y++) {
                    if (me.getSource().equals(buttons[x][y]) && !buttons[x][y].getText().equals("")) {
                        if (left_right_condition(x, y)) {
                            left_right(x, y);
                        }

                    }
                }
            }
            left_press = false;
            right_press = false;
        }
    }

    @Override
    public void mouseReleased(MouseEvent me) {
        if (me.getButton() == MouseEvent.BUTTON1) {
            left_press = false;
        } else if (me.getButton() == MouseEvent.BUTTON3) {
            right_press = false;
        }
    }

    @Override
    public void mouseEntered(MouseEvent me) {
    }

    @Override
    public void mouseExited(MouseEvent me) {
    }

    @Override
    public void keyTyped(KeyEvent ke) {
        if (ke.getKeyCode() == 113) {
            panel.removeAll();
            buttons();
        }
    }

    @Override
    public void keyPressed(KeyEvent ke) {
    }

    @Override
    public void keyReleased(KeyEvent ke) {
    }

    @Override
    public void itemStateChanged(ItemEvent ie) {
        if (ie.getStateChange() == ItemEvent.SELECTED) {
            if (ie.getSource() == Easy || ie.getSource() == Medium || ie.getSource() == Expert) {
                panel.removeAll();
                buttons();
            }
            if (ie.getSource() == Customized) {
                panel.removeAll();
                customized();
            }
        }
    }
}
