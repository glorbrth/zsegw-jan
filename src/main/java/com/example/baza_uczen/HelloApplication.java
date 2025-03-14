package com.example.baza_uczen;

import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.layout.*;
import javafx.stage.Stage;
import javafx.scene.control.*;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.VBox;


import java.sql.Connection;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.concurrent.atomic.AtomicReference;

public class HelloApplication extends Application {

    public static void main(String[] args) {
        launch();
    }

    @Override
    public void start(Stage stage) throws Exception {
        Connection connection = DBmanager.connectDB("jdbc:mysql://localhost:3306/school");

        //SELECT DATA
        Button selectButton = new Button("Wyświetl dane");
        TextField tableNameSelectField = new TextField("");

        selectButton.addEventHandler(MouseEvent.MOUSE_CLICKED, mouseEvent -> {
            System.out.println(DBmanager.select(connection,tableNameSelectField.getText()));
            GridPane gridPane = new GridPane();
            gridPane.setMinSize(400, 200);
            gridPane.setPadding(new Insets(10, 10, 10, 10));
            gridPane.setVgap(5);
            gridPane.setHgap(5);
            gridPane.setAlignment(Pos.CENTER);
            HashMap<Integer,String> data = DBmanager.select(connection,tableNameSelectField.getText());
            for(int i = 0; i<data.size();i++){
                Label text = new Label(data.get(i));
                gridPane.add(text,0,i);
            }

            Scene newScene = new Scene(gridPane,1000,500);

            Stage newWindow = new Stage();
            newWindow.setTitle("Wyświetlanie "+tableNameSelectField.getText());
            newWindow.setScene(newScene);

            newWindow.show();
        });

        HBox selectBox = new HBox();
        selectBox.getChildren().addAll(selectButton, tableNameSelectField);

        //END OF SELECT

        //INSERT DATA
        Button insertButton = new Button("Dodaj dane");
        TextField tableNameInsertField = new TextField("");

        insertButton.addEventHandler(MouseEvent.MOUSE_CLICKED, mouseEvent -> {
            System.out.println(DBmanager.select(connection,tableNameInsertField.getText()));
            GridPane gridPane = new GridPane();
            gridPane.setMinSize(400, 200);
            gridPane.setPadding(new Insets(10, 10, 10, 10));
            gridPane.setVgap(5);
            gridPane.setHgap(5);
            gridPane.setAlignment(Pos.TOP_CENTER);
            int cols = Integer.parseInt(DBmanager.getAmmountOfRows(connection, tableNameInsertField.getText()));
            ArrayList<String> colNames = DBmanager.getTableCols(connection,tableNameInsertField.getText(),cols);
            System.out.println(colNames);
            ArrayList<TextField> txtArray = new ArrayList<>();
            for(int i = 0; i<cols;i++){
                Label textLbl = new Label(colNames.get(i));
                TextField text = new TextField();
                txtArray.add(text);
                gridPane.add(textLbl,i,0);
                gridPane.add(text,i,1);
            }
            Button insertData = new Button("Zatwierdz dane");
            insertData.addEventHandler(MouseEvent.MOUSE_CLICKED, mouseEvent1 -> {
                String query = "INSERT INTO "+tableNameInsertField.getText()+" VALUES(";
                for(int i = 0; i<txtArray.size();i++){
                    query+="'"+txtArray.get(i).getText()+"'";
                    if(i!=txtArray.size()-1){
                        query+=", ";
                    }
                }
                query+=");";
                DBmanager.executeInsert(connection,query);
                System.out.println(query);
            });
            gridPane.add(insertData,0,2);


            Scene newScene = new Scene(gridPane,1000,500);

            Stage newWindow = new Stage();
            newWindow.setTitle("Dodawanie do "+tableNameInsertField.getText());
            newWindow.setScene(newScene);

            newWindow.show();
        });

        HBox insertBox = new HBox();
        insertBox.getChildren().addAll(insertButton, tableNameInsertField);
        //END OF INSERTING DATA

        //UPDATE DATA
        Button updateButton = new Button("Aktualizuj dane");
        TextField tableNameUpdateField = new TextField("");

        updateButton.addEventHandler(MouseEvent.MOUSE_CLICKED, mouseEvent -> {
            GridPane gridPane = new GridPane();
            gridPane.setMinSize(400, 200);
            gridPane.setPadding(new Insets(10, 10, 10, 10));
            gridPane.setVgap(5);
            gridPane.setHgap(5);
            gridPane.setAlignment(Pos.TOP_CENTER);

            //ADD SET COLUMNS
            int cols = Integer.parseInt(DBmanager.getAmmountOfRows(connection, tableNameInsertField.getText()));
            ArrayList<String> colNames = DBmanager.getTableCols(connection,tableNameUpdateField.getText(),cols);
            ArrayList<ComboBox> comboBoxes = new ArrayList<>();
            ArrayList<TextField> textFields = new ArrayList<>();

            Label setLabel = new Label("SET/USTAW: ");
            gridPane.add(setLabel,1,0);

            ComboBox comboBox = new ComboBox(FXCollections.observableArrayList(colNames));
            gridPane.add(comboBox,2,0);
            comboBoxes.add(comboBox);

            Label equalLabel = new Label(" = ");
            gridPane.add(equalLabel,3,0);

            TextField textField = new TextField();
            gridPane.add(textField,4,0);
            textFields.add(textField);


            Button addMoreSetFields = new Button("Dodaj wiecej");
            addMoreSetFields.addEventHandler(MouseEvent.MOUSE_CLICKED, mouseEvent2 -> {
                Integer n = comboBoxes.size() * 3;
                n+=2;
                ComboBox cbx = new ComboBox(FXCollections.observableArrayList(colNames));
                gridPane.add(cbx, n,0);
                comboBoxes.add(cbx);

                Label eqLabel = new Label(" = ");
                gridPane.add(eqLabel, n+1,0);

                TextField txtField = new TextField();
                gridPane.add(txtField, n+2,0);
                textFields.add(txtField);
            });
            gridPane.add(addMoreSetFields,0,0);

            //ADD WHERE CONDITIONS
            ArrayList<ComboBox> comboBoxesWhere = new ArrayList<>();
            ArrayList<TextField> textFieldsWhere = new ArrayList<>();

            Label setLabelWhere = new Label("WHERE/GDY: ");
            gridPane.add(setLabelWhere,1,1);

            ComboBox comboBoxWhere = new ComboBox(FXCollections.observableArrayList(colNames));
            gridPane.add(comboBoxWhere,2,1);
            comboBoxesWhere.add(comboBoxWhere);

            Label equalLabelWhere = new Label(" = ");
            gridPane.add(equalLabelWhere,3,1);

            TextField textFieldWhere = new TextField();
            gridPane.add(textFieldWhere,4,1);
            textFieldsWhere.add(textFieldWhere);


            Button addMoreWhereFields = new Button("Dodaj wiecej");
            addMoreWhereFields.addEventHandler(MouseEvent.MOUSE_CLICKED, mouseEvent3 -> {
                Integer n = comboBoxesWhere.size() * 3;
                n+=2;
                ComboBox cbx = new ComboBox(FXCollections.observableArrayList(colNames));
                gridPane.add(cbx, n,1);
                comboBoxesWhere.add(cbx);

                Label eqLabel = new Label(" = ");
                gridPane.add(eqLabel, n+1,1);

                TextField txtField = new TextField();
                gridPane.add(txtField, n+2,1);
                textFieldsWhere.add(txtField);
            });
            gridPane.add(addMoreWhereFields,0,1);


            Button updateData = new Button("Aktualizuj dane");
            updateData.addEventHandler(MouseEvent.MOUSE_CLICKED, mouseEvent1 -> {
                String query = "UPDATE "+tableNameUpdateField.getText()+" SET ";

                for(int i = 0; i<textFields.size(); i++) {
                    Object val = comboBoxes.get(i).getValue();
                    System.out.println(val);
                    if(val == null) continue;

                    String txt = textFields.get(i).getText();
                    if(txt.isEmpty()) continue;
                    //
                    query += val + "='" + txt + "'";
                    //add comma if not end
                    if(i != textFields.size()-1){
                        query+=",";
                    }
                }
                query+=" WHERE ";
                for(int i = 0; i<textFieldsWhere.size(); i++) {
                    Object val = comboBoxesWhere.get(i).getValue();
                    if(val == null) continue;
                    String txt = textFieldsWhere.get(i).getText();
                    if(txt.isEmpty()) continue;
                    query += val + "='" + txt + "'";
                    if(i != textFieldsWhere.size()-1){
                        query+=",";
                    }
                }
                query+=";";

                DBmanager.executeUpdate(connection,query);
                System.out.println(query);
            });
            gridPane.add(updateData,0,2);


            Scene newScene = new Scene(gridPane,1000,500);

            Stage newWindow = new Stage();
            newWindow.setTitle("Dodawanie do "+tableNameUpdateField.getText());
            newWindow.setScene(newScene);

            newWindow.show();
        });

        HBox updateBox = new HBox();
        updateBox.getChildren().addAll(updateButton, tableNameUpdateField);
        //END OF UPDATE DATA

        //DELETE DATA
        Button deleteButton = new Button("Usuń dane");
        TextField tableNameDeleteField = new TextField("");

        deleteButton.addEventHandler(MouseEvent.MOUSE_CLICKED, mouseEvent -> {
            GridPane gridPane = new GridPane();
            gridPane.setMinSize(400, 200);
            gridPane.setPadding(new Insets(10, 10, 10, 10));
            gridPane.setVgap(5);
            gridPane.setHgap(5);
            gridPane.setAlignment(Pos.TOP_CENTER);

            //ADD WHERE CONDITIONS
            int cols = Integer.parseInt(DBmanager.getAmmountOfRows(connection, tableNameDeleteField.getText()));
            ArrayList<String> colNames = DBmanager.getTableCols(connection,tableNameDeleteField.getText(),cols);
            ArrayList<ComboBox> comboBoxesWhere = new ArrayList<>();
            ArrayList<TextField> textFieldsWhere = new ArrayList<>();

            Label setLabelWhere = new Label("WHERE/GDY: ");
            gridPane.add(setLabelWhere,1,1);

            ComboBox comboBoxWhere = new ComboBox(FXCollections.observableArrayList(colNames));
            gridPane.add(comboBoxWhere,2,1);
            comboBoxesWhere.add(comboBoxWhere);

            Label equalLabelWhere = new Label(" = ");
            gridPane.add(equalLabelWhere,3,1);

            TextField textFieldWhere = new TextField();
            gridPane.add(textFieldWhere,4,1);
            textFieldsWhere.add(textFieldWhere);


            Button addMoreWhereFields = new Button("Dodaj wiecej");
            addMoreWhereFields.addEventHandler(MouseEvent.MOUSE_CLICKED, mouseEvent3 -> {
                Integer n = comboBoxesWhere.size() * 3;
                n+=2;
                ComboBox cbx = new ComboBox(FXCollections.observableArrayList(colNames));
                gridPane.add(cbx, n,1);
                comboBoxesWhere.add(cbx);

                Label eqLabel = new Label(" = ");
                gridPane.add(eqLabel, n+1,1);

                TextField txtField = new TextField();
                gridPane.add(txtField, n+2,1);
                textFieldsWhere.add(txtField);
            });
            gridPane.add(addMoreWhereFields,0,1);


            Button deleteData = new Button("Usuń dane");
            deleteData.addEventHandler(MouseEvent.MOUSE_CLICKED, mouseEvent1 -> {
                String query = "DELETE FROM "+tableNameDeleteField.getText()+" WHERE ";
                for(int i = 0; i<textFieldsWhere.size(); i++) {
                    Object val = comboBoxesWhere.get(i).getValue();
                    if(val == null) continue;
                    String txt = textFieldsWhere.get(i).getText();
                    if(txt.isEmpty()) continue;
                    if(i == 0){
                        query+=val + "='" + txt + "'";
                    } else {
                        query += ","+val + "='" + txt + "'";
                    }

                }
                query+=";";

                DBmanager.executeDelete(connection,query);
                System.out.println(query);
            });
            gridPane.add(deleteData,0,2);


            Scene newScene = new Scene(gridPane,1000,500);

            Stage newWindow = new Stage();
            newWindow.setTitle("Dodawanie do "+tableNameDeleteField.getText());
            newWindow.setScene(newScene);

            newWindow.show();
        });

        HBox deleteBox = new HBox();
        deleteBox.getChildren().addAll(deleteButton, tableNameDeleteField);
        //END OF DELETE

        //CREATE TABLE
        Button createButton = new Button("Dodaj tabele");
        TextField tableNameCreateField = new TextField("");

        createButton.addEventHandler(MouseEvent.MOUSE_CLICKED, mouseEvent -> {
            GridPane gridPane = new GridPane();
            gridPane.setMinSize(400, 200);
            gridPane.setPadding(new Insets(10, 10, 10, 10));
            gridPane.setVgap(5);
            gridPane.setHgap(5);
            gridPane.setAlignment(Pos.TOP_CENTER);

            //ADD WHERE CONDITIONS
            String types[] = {"INT","VARCHAR","BOOL"};

            ArrayList<TextField> fields = new ArrayList<>();
            ArrayList<TextField> sizes = new ArrayList<>();
            ArrayList<ComboBox> boxes = new ArrayList<>();

            ComboBox comboBox = new ComboBox(FXCollections.observableArrayList(types));
            gridPane.add(comboBox,1,1);
            boxes.add(comboBox);

            TextField txtField = new TextField();
            gridPane.add(txtField,0,1);
            fields.add(txtField);

            TextField sizeF = new TextField();
            gridPane.add(sizeF, 2,1);
            sizes.add(sizeF);


            Button addMoreWhereFields = new Button("Dodaj wiecej pol");
            addMoreWhereFields.addEventHandler(MouseEvent.MOUSE_CLICKED, mouseEvent3 -> {
                Integer n = boxes.size();
                n++;
                ComboBox cbx = new ComboBox(FXCollections.observableArrayList(types));
                gridPane.add(cbx, 1,n);
                boxes.add(cbx);

                TextField txt = new TextField();
                gridPane.add(txt, 0,n);
                fields.add(txt);

                TextField size = new TextField();
                gridPane.add(size, 2,n);
                sizes.add(size);
            });
            gridPane.add(addMoreWhereFields,0,0);


            Button createTable = new Button("Generuj tabele");
            createTable.addEventHandler(MouseEvent.MOUSE_CLICKED, mouseEvent1 -> {
                String query = "CREATE TABLe "+tableNameCreateField.getText()+" ( ";
                for(int i = 0; i<fields.size(); i++) {
                    Object val = boxes.get(i).getValue();
                    if(val == null) continue;
                    String txt = fields.get(i).getText();
                    if(txt.isEmpty()) continue;
                    String size = sizes.get(i).getText();
                    if(!size.isEmpty()) { val+="("+size+")"; }
                    if(i == 0){
                        query+= txt + " " + val;
                    } else {
                        query += ","+txt + " " + val;
                    }

                }
                query+=");";

                DBmanager.createTable(connection,query);
                System.out.println(query);
            });
            gridPane.add(createTable,2,0);


            Scene newScene = new Scene(gridPane,1000,500);

            Stage newWindow = new Stage();
            newWindow.setTitle("Dodawanie do "+tableNameCreateField.getText());
            newWindow.setScene(newScene);

            newWindow.show();
        });

        HBox createBox = new HBox();
        createBox.getChildren().addAll(createButton, tableNameCreateField);
        //END CREATE TABLE

        //DROP TABLE
        Button dropButton = new Button("Usuń tabele");
        TextField tableNameDropField = new TextField("");

        dropButton.addEventHandler(MouseEvent.MOUSE_CLICKED, mouseEvent -> {
            DBmanager.dropTable(connection,tableNameDropField.getText());
        });

        HBox dropBox = new HBox();
        dropBox.getChildren().addAll(dropButton, tableNameDropField);


        VBox vBox = new VBox();
        vBox.getChildren().addAll(selectBox,insertBox,updateBox, deleteBox, createBox, dropBox);

        Scene scene = new Scene(vBox, 320, 240);
        stage.setTitle("edytor tekstu");
        stage.setScene(scene);
        stage.show();
    }
}