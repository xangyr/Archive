/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.Graphics;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import javax.swing.*;
import javax.swing.event.TableModelEvent;
import javax.swing.event.TableModelListener;
import proj_3.sql_inter;

/**
 *
 * @author xvr5040
 */
enum days {
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY;
}

public class login_menu implements ActionListener, TableModelListener {

    JFrame frame;
    JPanel initiate;
    JPanel log;
    JPanel manager_pane;
    JPanel user_pane;

    JTable table;
    boolean Logged = false;

    public login_menu() {
        frame = new JFrame("Find Stores");

        init_page();
        //login_page();

        frame.setSize(350, 250);
        frame.setVisible(true);

        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }

    public void init_page() {
        frame.setLayout(new BorderLayout());
        initiate = new JPanel();
        initiate.setVisible(true);
        initiate.setLayout(new GridLayout(1, 2, 2, 0));

        frame.getContentPane().add(initiate);
        initiate.setSize(frame.getSize());

        JButton manager_btn = new JButton("Manager Login");
        JButton guest_btn = new JButton("Guest Portal");

        initiate.add(manager_btn);
        initiate.add(guest_btn);

        manager_btn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                login_page();
                frame.setSize(350, 200);
                initiate.setVisible(false);
                //log.setVisible(true);
            }
        });

        guest_btn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                Logged = false;
                user_port();
            }

        });

    }

    public void login_page() {
        frame.setLayout(new FlowLayout());

        log = new JPanel();
        log.setVisible(true);

        frame.getContentPane().add(log);

        JButton back;
        JButton login;

        JPanel input_field = new JPanel(new GridLayout(2, 1, 15, 15));
        JPanel btn_field = new JPanel(new BorderLayout());

        JPanel usrname = new JPanel(new FlowLayout());
        JPanel pswd = new JPanel(new FlowLayout());

        usrname.add(new JLabel("Username:"));

        JTextField usr_text = new JTextField(20);
        //usr_text.setColumns(10);

        JPasswordField pass = new JPasswordField(20);
        //pass.setColumns(20);

        pswd.add(new JLabel("Password:"));
        usrname.add(usr_text);
        pswd.add(pass);

        back = new JButton("Back");
        back.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                frame.remove(log);
                frame.getContentPane().add(initiate);
            }

        });
        login = new JButton("Log in");
        login.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                try {
                    String usr = usr_text.getText();
                    String str = "select * from managerlogon";                      //select statement
                    sql_inter sql = new sql_inter();
                    ResultSet rs = sql.get_data(str);

                    while (rs.next()) {
                        //System.out.println(rs.getString("password"));
                        if (usr.equals(rs.getString("username")) && String.valueOf(pass.getPassword()).equals(rs.getString("password"))) {
                            Logged = true;

                            break;
                        } else {
                            Logged = false;
                            //System.out.println("Failed. Can't find the username or the password is wrong");

                        }
                    }
                    if (Logged) {
                        System.out.println("Logged in...");
                        frame.setSize(1400, 300);
                        logged_in(usr);
                        usr_text.setText("");
                        pass.setText("");
                    } else {
                        JOptionPane.showMessageDialog(null, "Failed. Can't find the username or the password is wrong");
                    }
                    rs.close();
                    sql.close();
                } catch (SQLException ex) {
                    ex.printStackTrace();
                }

            }

        });

        btn_field.add(login, BorderLayout.EAST);
        btn_field.add(back, BorderLayout.WEST);

        input_field.add(usrname);
        input_field.add(pswd);

        log.setLayout(new BorderLayout());

        log.add(input_field, BorderLayout.CENTER);
        log.add(btn_field, BorderLayout.SOUTH);
        frame.validate();
    }

    public void logged_in(String usr) {

        manager_pane = new JPanel(new BorderLayout());
        log.setVisible(false);

        //manager_pane.setVisible(true);
        frame.getContentPane().add(manager_pane);
        manager_pane.setSize(frame.getSize());

        JButton back = new JButton("Back");
        back.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                manager_pane.setVisible(false);
                log.setVisible(true);
                frame.setSize(350, 150);
                Logged = false;
                table.removeAll();
            }
        });

        manager_pane.add(back, BorderLayout.SOUTH);

        String[] COLS = new String[11];
        Object[][] data = new Object[11][11];

        try {
            //TODO add store hours to the select query 
            String str = "select (select store_name from stores where store_id = m.store_id) store_name, "
                    + "(select address from stores where store_id = m.store_id) address, "
                    + "(select description from stores where store_id = m.store_id) description, "
                    + "(select zip from stores where store_id = m.store_id) zipcode, ";
            for (int i = 1; i < 7; i++) {
                str += "(select open_time from store_hours where store_id = m.store_id and day = "
                        + i + ") open_time_" + i + ", ";
                str += "(select close_time from store_hours where store_id = m.store_id and day = "
                        + i + ") clsoe_time_" + i + ", ";
            }
            str += "(select open_time from store_hours where store_id = m.store_id and day = 7)  open_time_7, ";
            str += "(select close_time from store_hours where store_id = m.store_id and day = 7) close_time_7 ";

            str += "from managerlogon m where username = '" + usr + "'";                      //select statement, didn't add store hours this time

            System.out.println(str);
            sql_inter sql = new sql_inter();
            ResultSet rs = sql.get_data(str);
            ResultSetMetaData metaData = rs.getMetaData();
            for (int i = 0; i < 4; i++) {
                COLS[i] = metaData.getColumnName(i + 1);
            }
            days[] day = days.values();

            for (int i = 4; i < 11; i++) {
                COLS[i] = day[i - 4].name();
            }

            table = new JTable(data, COLS);

            int row = 0;
            while (rs.next()) {
                for (int i = 0; i < 4; i++) {
                    table.setValueAt(rs.getString(i + 1), row, i);

                }

                /*
                table.setValueAt(rs.getString(1), row, 0);
                table.setValueAt(rs.getString(2), row, 1);
                table.setValueAt(rs.getString(3), row, 2);
                table.setValueAt(rs.getString(4), row, 3);
                 */
                for (int i = 0; i < 14; i += 2) {
                    table.setValueAt(rs.getString(i + 5) + "~" + rs.getString(i + 6), row, i / 2 + 4);

                }

                row++;
            }
            //table.getColumn(2).setWidth(table.getColumn(2).getWidth()+25);
            table.setAutoResizeMode(JTable.AUTO_RESIZE_OFF);
            table.getModel().addTableModelListener(this);

            JPanel tablePanel = new JPanel(new BorderLayout());

            manager_pane.add(new JScrollPane(table));
            tablePanel.add(table.getTableHeader(), BorderLayout.NORTH);
            tablePanel.add(table, BorderLayout.CENTER);
            manager_pane.add(tablePanel, BorderLayout.CENTER);

            rs.close();
            sql.close();
        } catch (SQLException ex) {
            ex.printStackTrace();
        }

        frame.validate();
    }

    public void user_port() {
        user_pane = new JPanel(new BorderLayout());
        frame.getContentPane().add(user_pane);
        initiate.setVisible(false);
        user_pane.setVisible(true);

        JRadioButton by_state = new JRadioButton();
        JLabel state_label = new JLabel("Search by States: ");
        JRadioButton by_zip = new JRadioButton();
        JLabel zip_label = new JLabel("Search by Zipcodes: ");

    }

    public static void main(String[] args) {
        new login_menu();
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        frame.validate();
        frame.repaint();
    }

    @Override
    public void tableChanged(TableModelEvent e) {
        //System.out.println("Table changed");

    }
}
