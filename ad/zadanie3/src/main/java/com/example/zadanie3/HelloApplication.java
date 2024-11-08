package com.example.zadanie3;

import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.EventType;
import javafx.fxml.FXMLLoader;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Node;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.stage.Stage;

import javax.swing.*;
import java.io.IOException;

public class HelloApplication extends Application {
    @Override
    public void start(Stage stage) throws IOException {
        Label metodaLabel = new Label();
        metodaLabel.setGraphic(new Label(" metoda obliczen "));
        metodaLabel.getGraphic().setStyle("-fx-background-color: #f4f4f4;");

        ToggleGroup metodaObliczen = new ToggleGroup();
        RadioButton netto = new RadioButton("Od netto do brutto");
        netto.setToggleGroup(metodaObliczen);
        RadioButton brutto = new RadioButton("Od brutto do netto");
        brutto.setToggleGroup(metodaObliczen);
        RadioButton vat = new RadioButton("Dopasuj do kwoty VAT");
        vat.setToggleGroup(metodaObliczen);

        GridPane metodaPane = new GridPane();
        metodaPane.setMinSize(300, 100);
        metodaPane.setPadding(new Insets(10, 10, 10, 10));
        metodaPane.setVgap(5);
        metodaPane.setHgap(5);
        metodaPane.setAlignment(Pos.CENTER);

        metodaPane.add(metodaLabel,0,0);
        metodaPane.add(netto,0,1);
        metodaPane.add(brutto,0,2);
        metodaPane.add(vat,0,3);


        Label daneLabel = new Label("Dane: ");
        Label wartoscLabel = new Label("Wartość bazowa:");
        TextField wartoscField = new TextField();
        Label vatLabel = new Label("Stawka VAT:");
        ChoiceBox vatBox = new ChoiceBox();
        vatBox.getItems().addAll
                ("23%", "14%", "7%", "5%");


        GridPane danePane = new GridPane();
        danePane.setMinSize(300,100);
        danePane.setPadding(new Insets(10, 10, 10, 10));
        danePane.setVgap(5);
        danePane.setHgap(5);
        danePane.setAlignment(Pos.CENTER);


        danePane.add(daneLabel,0,0);
        danePane.add(wartoscLabel,0,1);
        danePane.add(wartoscField,1,1);
        danePane.add(vatLabel,0,2);
        danePane.add(vatBox,1,2);

        Button obliczBtn = new Button("OBLICZ");
        obliczBtn.addEventHandler(MouseEvent.MOUSE_CLICKED, (e)->{

        });

        Button zamknijBtn = new Button("ZAMKNIJ");
        zamknijBtn.addEventHandler(MouseEvent.MOUSE_CLICKED, (e)->{

        });




        GridPane gridPane = new GridPane();
        gridPane.setMinSize(500, 500);
        gridPane.setPadding(new Insets(10, 10, 10, 10));
        gridPane.setVgap(5);
        gridPane.setHgap(5);
        gridPane.setAlignment(Pos.CENTER);

        gridPane.add(metodaPane,0,0);
        gridPane.add(danePane,0,1);
        gridPane.add(obliczBtn,0,2);
        gridPane.add(zamknijBtn,2,2);
        Scene scene = new Scene(gridPane);
        stage.setTitle("Hello!");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}