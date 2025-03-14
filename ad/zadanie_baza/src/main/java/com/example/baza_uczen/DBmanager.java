package com.example.baza_uczen;

import com.mysql.cj.xdevapi.JsonArray;
import com.mysql.cj.xdevapi.JsonString;
import netscape.javascript.JSObject;

import java.sql.*;
import java.util.ArrayList;
import java.util.HashMap;

public class DBmanager {

    public static final String url = "jdbc:mysql://localhost:3306/school";

    public static Connection connectDB(String url) {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }

        Connection connection = null;

        try {
            String username = "root";
            String password = "";

            connection = DriverManager.getConnection(url, username, password);

        } catch (SQLException e) {
            e.printStackTrace();
        }
        return connection;
    }


    public static void executeQuery(Connection connection, String query) {
        try {
            Statement statement = connection.createStatement();
            ResultSet resultSet = statement.executeQuery(query);
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public static void executeInsert(Connection connection, String query) {
        try {
            Statement statement = connection.createStatement();
            int rowsInserted = statement.executeUpdate(query);
            if (rowsInserted > 0) {
                System.out.println("A new user was inserted successfully!");
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public static void executeUpdate(Connection connection, String query) {
        try {
            Statement statement = connection.createStatement();
            int rowsUpdated = statement.executeUpdate(query);
            if (rowsUpdated > 0) {
                System.out.println("Updated successfully!");
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public static void executeDelete(Connection connection, String query) {
        try {
            Statement statement = connection.createStatement();
            int rowsUpdated = statement.executeUpdate(query);
            if (rowsUpdated > 0) {
                System.out.println("Deleted successfully!");
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public static void createTable(Connection connection, String query) {
        try {
            Statement statement = connection.createStatement();
            int rowsUpdated = statement.executeUpdate(query);
            if (rowsUpdated > 0) {
                System.out.println("Created successfully!");
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public static void dropTable(Connection connection, String tableName) {
        try {
            Statement statement = connection.createStatement();
            int rowsUpdated = statement.executeUpdate("DROP TABLE "+tableName);
            if (rowsUpdated > 0) {
                System.out.println("Dropped successfully!");
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }


    public static String getAmmountOfRows(Connection connection, String tableName) {
        String count = "";
        try {
            Statement statement = connection.createStatement();
            ResultSet resultSet = statement.executeQuery("SELECT Count(*) FROM INFORMATION_SCHEMA.Columns where TABLE_NAME = '" + tableName + "'");
            resultSet.next();
            System.out.println(resultSet.getString(1));
            count = resultSet.getString(1);
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return count;
    }

    public static ArrayList<String> getTableCols(Connection connection, String tableName, Integer cols) {
        ArrayList<String> res = new ArrayList<>();
        try {
            Statement statement = connection.createStatement();
            ResultSet resultSet = statement.executeQuery("DESCRIBE " + tableName);
            while (resultSet.next()) {
                res.add(resultSet.getString(1));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return res;
    }

    public static HashMap<Integer, String> select(Connection connection, String tableName) {
        StringBuilder res = null;
        HashMap<Integer, String> result = new HashMap<Integer, String>();
        try {
            Statement statement = connection.createStatement();
            //get data about columns, their names and data types
            //resultSet = statement.executeQuery("DESCRIBE " + tableName);

            ResultSet resultSet = statement.executeQuery("SELECT * FROM " + tableName);
            ResultSetMetaData rsmd = resultSet.getMetaData();

            res = new StringBuilder();

            int colCount = rsmd.getColumnCount();

            //add all rows
            int j = 1;
            while (resultSet.next()) {
                for (int i = 1; i <= colCount; i++) {
                    res.append(resultSet.getString(i) + " ");
                }
                result.put(j, String.valueOf(res));
                j++;
                res.setLength(0);
            }

            resultSet = statement.executeQuery("DESCRIBE " + tableName);
            while (resultSet.next()) {
                res.append(resultSet.getString(1) + " ");
            }
            result.put(0, String.valueOf(res));

        } catch (SQLException e) {
            e.printStackTrace();
        }
        return result;
    }
}
