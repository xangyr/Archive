/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


/**
 *
 * @author xvr5040
 */

import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;
import java.sql.*;
import javax.swing.JTable;

public class sql_inter {
    // JDBC driver name and database URL

    static final String JDBC_DRIVER = "org.apache.derby.jdbc.ClientDriver";
    static final String DB_URL = "jdbc:derby://localhost:1527/final";

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

    public void insert(String sql) {
        
        try {
            stmt.executeUpdate(sql);
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
