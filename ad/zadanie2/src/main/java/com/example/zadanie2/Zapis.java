package com.example.zadanie2;

import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.EventType;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.GridPane;
import javafx.scene.text.Text;
import javafx.stage.Stage;

public class Zapis extends Application {
    @Override
    public void start(Stage stage) {
        Text imieLabel = new Text("Imie");

        TextField imieText = new TextField();

        Text dataUrodzin = new Text("Data urodzin");

        DatePicker wyborDataUrodzin = new DatePicker();

        Text plecLabel = new Text("Płeć");

        ToggleGroup grupaPlec = new ToggleGroup();
        RadioButton mezczyznaRadio = new RadioButton("mężczyzna");
        mezczyznaRadio.setToggleGroup(grupaPlec);
        RadioButton kobietaRadio = new RadioButton("kobieta");
        kobietaRadio.setToggleGroup(grupaPlec);

        Text rezerwacjaLabel = new Text("Rezerwacja");

        ToggleButton Rezerwacje = new ToggleButton();
        ToggleButton yes = new ToggleButton("Tak");
        ToggleButton no = new ToggleButton("Nie");
        ToggleGroup groupReservation = new ToggleGroup();
        yes.setToggleGroup(groupReservation);
        no.setToggleGroup(groupReservation);

        Text technologieLabel = new Text("Znane technologie");

        CheckBox jezykJavaCB = new CheckBox("Java");
        jezykJavaCB.setIndeterminate(false);

        CheckBox jezykCCB = new CheckBox("C");
        jezykJavaCB.setIndeterminate(false);

        Text kwalifikacjeLabel = new Text("Kwalifikacje");

        ObservableList<String> list = FXCollections.observableArrayList(
                "Inżynier", "Magister", "Doktor", "Podyplomowe");
        ListView<String> listaKwalifikacji = new ListView<String>(list);
        listaKwalifikacji.setMaxSize(200,50);

        Text lokalizacjaLabel = new Text("Lokalizacja");

        ChoiceBox lokacjaCB = new ChoiceBox();
        lokacjaCB.getItems().addAll
                ("Wrocław", "Kraków", "Lwów", "Poznań", "Gdańsk");

        Button rejstracjaBtn = new Button("Zarejstruj się");

        rejstracjaBtn.addEventHandler(MouseEvent.MOUSE_CLICKED,(e)->{
            Alert alert = new Alert(Alert.AlertType.WARNING);
            alert.setTitle("Potwierdzenie");
            alert.setHeaderText("ZAREJSTROWANO:");
            RadioButton selectedRadioButton = (RadioButton) grupaPlec.getSelectedToggle();
            String plecGroupValue = selectedRadioButton.getText();

            ToggleButton selectedReservation = (ToggleButton) groupReservation.getSelectedToggle();
            String reservationValue = selectedReservation.getText();

            String technologie = "";
            if(jezykJavaCB.isSelected()) {
                technologie += "Java ";
            }
            if (jezykCCB.isSelected()) {
                technologie += "C";
            }
            if (technologie == ""){
                technologie = "brak";
            }

            alert.setContentText(
                    "imie: " + imieText.getText() + "\ndata urodzenia: " + wyborDataUrodzin.getValue() + "\nplec: " + plecGroupValue + "\nrezerwacja: " +
                            reservationValue + "\ntechnologie: " + technologie + "\nkwalifikacje:? " + listaKwalifikacji.getFocusModel() +
                            "\nlokacja: " + lokacjaCB.getValue()
            );
            alert.show();
        });

        GridPane gridPane = new GridPane();

        gridPane.setMaxSize(500, 500);

        gridPane.setPadding(new Insets(10, 10, 10, 10));

        gridPane.setVgap(5);
        gridPane.setHgap(5);

        gridPane.setAlignment(Pos.CENTER);

        gridPane.add(imieLabel, 0, 0);
        gridPane.add(imieText, 1, 0);

        gridPane.add(dataUrodzin, 0, 1);
        gridPane.add(wyborDataUrodzin, 1, 1);

        gridPane.add(plecLabel, 0, 2);
        gridPane.add(mezczyznaRadio, 1, 2);
        gridPane.add(kobietaRadio, 2, 2);
        gridPane.add(rezerwacjaLabel, 0, 3);
        gridPane.add(yes, 1, 3);
        gridPane.add(no, 2, 3);

        gridPane.add(technologieLabel, 0, 4);
        gridPane.add(jezykJavaCB, 1, 4);
        gridPane.add(jezykCCB, 2, 4);

        gridPane.add(kwalifikacjeLabel, 0, 5);
        gridPane.add(listaKwalifikacji, 1, 5);

        gridPane.add(lokalizacjaLabel, 0, 6);
        gridPane.add(lokacjaCB, 1, 6);

        gridPane.add(rejstracjaBtn, 2, 8);

        rejstracjaBtn.setStyle(
                "-fx-background-color: darkslateblue; -fx-textfill: white;");

        imieLabel.setStyle("-fx-font: normal bold 15px 'serif' ");
        dataUrodzin.setStyle("-fx-font: normal bold 15px 'serif' ");
        plecLabel.setStyle("-fx-font: normal bold 15px 'serif' ");
        rezerwacjaLabel.setStyle("-fx-font: normal bold 15px 'serif' ");
        technologieLabel.setStyle("-fx-font: normal bold 15px 'serif' ");
        kwalifikacjeLabel.setStyle("-fx-font: normal bold 15px 'serif' ");
        lokalizacjaLabel.setStyle("-fx-font: normal bold 15px 'serif' ");

        gridPane.setStyle("-fx-background-color: BEIGE;");

        Scene scene = new Scene(gridPane);

        stage.setTitle("Registration Form");

        stage.setScene(scene);

        stage.show();
    }
    public static void main(String args[]){
        launch(args);
    }
}