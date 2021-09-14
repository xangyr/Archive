package proj_3;

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
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.*;
import javax.swing.event.TableModelEvent;
import javax.swing.event.TableModelListener;
import javax.swing.table.TableModel;
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

    JTable table_manager;
    JTable table_usr;
    boolean Logged = false;
    sql_inter sql;
    String title = "Find Stores";
    String[] COLS = {"STORE NAME", "ADDRESS", "DESCRIPTION", "ZIPCODE", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"};
    boolean is_zip = false;
    String table_query;
    
    double lo;
    double la;

    public login_menu() {
        frame = new JFrame(title);

        init_page();
        //login_page();

        sql = new sql_inter();

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
                frame.setSize(1400, 500);
                initiate.setVisible(false);
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
                frame.setLayout(new BorderLayout());
                log.setVisible(false);
                initiate.setVisible(true);
                frame.getContentPane().add(initiate);
                frame.setSize(350, 250);
            }

        });
        login = new JButton("Log in");
        login.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                try {
                    String usr = usr_text.getText();
                    String str = "select * from managerlogon";                      //select statement
                    //sql_inter sql = new sql_inter();
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
                        frame.setTitle(title + " Logged in...");
                        //System.out.println("Logged in...");
                        frame.setSize(1400, 300);
                        logged_in(usr);
                        usr_text.setText("");
                        pass.setText("");
                    } else {
                        JOptionPane.showMessageDialog(null, "Failed. Can't find the username or the password is wrong");
                    }

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
        frame.setLayout(new BorderLayout());
        frame.getContentPane().add(manager_pane);
        //manager_pane.setSize(frame.getSize());

        frame.setTitle(title + " connecting to database...");

        JButton back = new JButton("Back");
        back.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                manager_pane.setVisible(false);
                log.setVisible(true);
                frame.setSize(350, 200);
                Logged = false;
                table_manager.removeAll();
                frame.setTitle(title + " lose connection...");
            }
        });

        manager_pane.add(back, BorderLayout.SOUTH);

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
        str += "(select open_time from store_hours where store_id = m.store_id and day = 7) open_time_7, ";
        str += "(select close_time from store_hours where store_id = m.store_id and day = 7) close_time_7 ";

        str += "from managerlogon m where username = '" + usr + "'";                      //select statement, didn't add store hours this time

        //String[] COLS = new String[11];
        //Object[][] data = new Object[11][11];
        //try {
        //TODO add store hours to the select query 
        /*String str = "select (select store_name from stores where store_id = m.store_id) store_name, "
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

            //System.out.println(str);
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

                
                table.setValueAt(rs.getString(1), row, 0);
                table.setValueAt(rs.getString(2), row, 1);
                table.setValueAt(rs.getString(3), row, 2);
                table.setValueAt(rs.getString(4), row, 3);
                 
                for (int i = 0; i < 14; i += 2) {
                    table.setValueAt(rs.getString(i + 5) + "~" + rs.getString(i + 6), row, i / 2 + 4);
                    
                }
                
                row++;
            }*/
        //table.getColumn(2).setWidth(table.getColumn(2).getWidth()+25);
        table_manager = sql.get_mana_table(str);
        table_manager.setAutoResizeMode(JTable.AUTO_RESIZE_OFF);
        table_manager.getModel().addTableModelListener(this);

        JPanel tablePanel = new JPanel(new BorderLayout());

        manager_pane.add(new JScrollPane(table_manager));
        tablePanel.add(table_manager.getTableHeader(), BorderLayout.NORTH);
        tablePanel.add(table_manager, BorderLayout.CENTER);
        manager_pane.add(tablePanel, BorderLayout.CENTER);

        /*rs.close();
            sql.close();
        } catch (SQLException ex) {
            ex.printStackTrace();
        }*/
        frame.setTitle(title + " connected...");
        frame.validate();
    }

    public void user_port() {
        frame.setLayout(new BorderLayout());
        user_pane = new JPanel(new BorderLayout());

        initiate.setVisible(false);
        user_pane.setVisible(true);
        frame.getContentPane().add(user_pane);

        JRadioButton by_state = new JRadioButton();
        JLabel state_label = new JLabel("Search by States: ");
        JRadioButton by_zip = new JRadioButton();
        JLabel zip_label = new JLabel("Search by Zipcodes: ");
        JTextField input = new JTextField(5);
        JLabel dis_label = new JLabel("Input distance: ");
        JTextField dis = new JTextField(8);
        JButton search = new JButton("Search");

        ButtonGroup searching = new ButtonGroup();
        searching.add(by_state);
        searching.add(by_zip);

        JPanel io_pane = new JPanel(new FlowLayout(FlowLayout.CENTER));
        
        dis.setText("0");
        dis.setToolTipText("Find Store by zip, default set distance to 0");
        dis.setEnabled(false);

        io_pane.add(by_state);
        io_pane.add(state_label);
        io_pane.add(by_zip);
        io_pane.add(zip_label);
        io_pane.add(input);
        io_pane.add(dis_label);
        io_pane.add(dis);
        io_pane.add(search);
        by_state.setSelected(true);

        table_query = "select store_name, address, description, zip, ";
        for (int i = 1; i < 7; i++) {
            table_query += "(select open_time from store_hours where store_id = s.store_id and day = "
                    + i + ") open_time_" + i + ", ";
            table_query += "(select close_time from store_hours where store_id = s.store_id and day = "
                    + i + ") clsoe_time_" + i + ", ";
        }
        table_query += "(select open_time from store_hours where store_id = s.store_id and day = 7) open_time_7, ";
        table_query += "(select close_time from store_hours where store_id = s.store_id and day = 7) close_time_7 ";

        Object[][] data = new Object[11][11];

        table_usr = new JTable(data, COLS);

        by_state.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                is_zip = false;
                dis.setEnabled(false);
                input.setText("");
            }
        });
                
        by_zip.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                is_zip = true;
                dis.setEnabled(true);
                input.setText("");
            } 
        });
        
        input.addActionListener(this); 
        dis.addActionListener(this);

        search.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                try {

                    Object[][] data = new Object[11][11];

                    table_usr = new JTable(data, COLS);
                    JPanel tablePanel = new JPanel(new BorderLayout());
                    user_pane.add(new JScrollPane(table_usr));
                    tablePanel.add(table_usr.getTableHeader(), BorderLayout.NORTH);
                    tablePanel.add(table_usr, BorderLayout.CENTER);
                    user_pane.add(tablePanel, BorderLayout.CENTER);
                    
                    frame.validate();
                    String str;
                    
                    if (is_zip) {
                        ResultSet dis_rs = sql.get_data("select longtitude, latitude from zipcodes where zip = '"+input.getText()+"'");
                        //double lo;
                        //double la = 0;
                        while (dis_rs.next()) {
                            lo = dis_rs.getDouble("longtitude");
                            la = dis_rs.getDouble("latitude");
                        }
                        str = "from stores s where s.zip in(select zip from stores where zip in(select zip from zipcodes z where 3956.55*acos(cos("+la+")*cos(z.latitude)*cos("+lo+"-z.longtitude)+sin("+la+")*sin(z.latitude)) <" + dis.getText()+"))";
                    } else {
                        str = "from stores s where s.ZIP in(select zip from zipcodes zi where zi.state in('" + input.getText() + "'))";
                    }
                    //System.out.println(table_query);
                    ResultSet rs = sql.get_data(table_query + str);
                    int row = 0;
                    while (rs.next()) {
                        //System.out.println(rs.getString(1));
                        for (int i = 0; i < 4; i++) {
                            table_usr.setValueAt(rs.getString(i + 1), row, i);

                        }

                        /*
                table.setValueAt(rs.getString(1), row, 0);
                table.setValueAt(rs.getString(2), row, 1);
                table.setValueAt(rs.getString(3), row, 2);
                table.setValueAt(rs.getString(4), row, 3);
                         */
                        for (int i = 0; i < 14; i += 2) {
                            table_usr.setValueAt(rs.getString(i + 5) + "~" + rs.getString(i + 6), row, i / 2 + 4);

                        }

                        row++;
                    }
                    //table.getColumn(2).setWidth(table.getColumn(2).getWidth()+25);
                    table_usr.setAutoResizeMode(JTable.AUTO_RESIZE_OFF);

                    //rs.close();
                    //sql.close();
                } catch (SQLException ex) {
                    ex.printStackTrace();
                }
            }
        });

        frame.repaint();
        //table.setAutoResizeMode(JTable.AUTO_RESIZE_OFF);
        user_pane.add(io_pane, BorderLayout.NORTH);

        JButton back = new JButton("Back");
        back.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                user_pane.setVisible(false);
                initiate.setVisible(true);
                frame.setSize(350, 250);
                Logged = false;
            }
        });

        user_pane.add(back, BorderLayout.SOUTH);

        frame.validate();
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
        int row = e.getFirstRow();
        int column = e.getColumn();
        TableModel model = (TableModel) e.getSource();
        Object data = model.getValueAt(row, column);
        int day = column -3;

        if (column > 3 && column < 11) {
            String str = "update store_hours set open_time = '" + data.toString().split("~")[0] + "', "
                    + "close_time = '" + data.toString().split("~")[1] + "' "
                    + "where store_id in(select store_id from stores where zip = '"+table_manager.getValueAt(row, 3)+"' and address = '" +table_manager.getValueAt(row, 1)+"') and day = "+ day;
            //System.out.println(str);
            sql.update(str);
        }

    }
}
