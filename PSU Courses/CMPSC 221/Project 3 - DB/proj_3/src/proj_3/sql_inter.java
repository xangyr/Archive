/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package proj_3;

/**
 *
 * @author xvr5040
 */
import java.awt.BorderLayout;
import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;
import java.sql.*;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;

public class sql_inter {
    // JDBC driver name and database URL

    static final String JDBC_DRIVER = "org.apache.derby.jdbc.ClientDriver";
    static final String DB_URL = "jdbc:derby://localhost:1527/project3";

    // Database credentials
    static final String USER = "root";
    static final String PASS = "root";

    String filename;

    Scanner input = null;
    String line;
    String[] elements;

    Connection conn = null;
    Statement stmt = null;

    public sql_inter() {

        try {
            Class.forName(JDBC_DRIVER);
            // Open a connection
            //System.out.println("Connecting to database...");

            conn = DriverManager.getConnection(DB_URL, USER, PASS);
            stmt = conn.createStatement();

        } catch (ClassNotFoundException ce) {
            ce.printStackTrace();
        } catch (SQLException se) {
            se.printStackTrace();
        }
        // Handle errors for JDBC
    }

    public void insert(String str) {
        filename = str;

        try {
            input = new Scanner(new File(filename));
            while (input.hasNext()) {
                String sql = "insert into zipcodes values (";
                line = input.nextLine().replaceAll("\"", "");
                elements = line.split(",");
                for (int i = 0; i < 5; i++) {
                    if (i < 3) {
                        elements[i] = "'" + elements[i] + "'";
                    }
                    sql += elements[i];
                    if (i < 4) {
                        sql += ", ";
                    }
                }
                sql += ")";
                stmt.executeUpdate(sql);

            }
            System.out.println("Inserted records into the table...");

        } catch (FileNotFoundException fe) {
            System.out.println("Please make sure you have a file called zipcodes.csv");
        } catch (SQLException ex) {
            ex.printStackTrace();
        }
    }

    public void update(String str) {
        try {
            stmt.executeUpdate(str);
        } catch (SQLException ex) {
            ex.printStackTrace();
        }
    }

    public ResultSet get_data(String sql) {
        ResultSet rs = null;
        try {
            rs = stmt.executeQuery(sql);
        } catch (SQLException ex) {
            ex.printStackTrace();
        }
        return rs;

    }

    public JTable get_mana_table(String str) {
        String[] COLS = {"STORE NAME", "ADDRESS", "DESCRIPTION", "ZIPCODE", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"};
        Object[][] data = new Object[11][11];

        JTable table = null;

        try {
            //System.out.println(str);
            sql_inter sql = new sql_inter();
            ResultSet rs = sql.get_data(str);

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

            //rs.close();
            //sql.close();
        } catch (SQLException ex) {
            ex.printStackTrace();
        }
        return table;
    }

    public JTable get_table(ResultSet rs) {
        String[] COLS = {"STORE NAME", "ADDRESS", "DESCRIPTION", "ZIPCODE", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"};
        Object[][] data = new Object[11][11];

        JTable table = null;

        try {
            //System.out.println(str);
            //sql_inter sql = new sql_inter();
            //ResultSet rs = sql.get_data(str);

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

            //rs.close();
            //sql.close();
        } catch (SQLException ex) {
            ex.printStackTrace();
        }
        return table;
    }

    public void close() {

        try {
            if (stmt != null) {
                conn.close();
            }
        } catch (SQLException se) {
        }// do nothing
        try {
            if (conn != null) {
                conn.close();
            }
        } catch (SQLException se) {
            se.printStackTrace();
        }
        try {
            stmt.close();
            conn.close();
        } catch (SQLException ex) {
            ex.printStackTrace();
        }

    }

    /**
     * @param args the command line arguments
     */
    /*public static void main(String[] args) {
        new sql_inter().insert("zipcodes.csv");
    }*/
}
