package com.example.zadanie3;


import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Node;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.*;
import javafx.stage.Stage;

import java.io.IOException;

//obramówka -> tytul w obramowce + węzły w obramówce
class BorderedTitledPane extends StackPane {
    static final int Y_OFFSET = 20;
    BorderedTitledPane(String title, Node content) {
        setStyle("-fx-border-color: #888888; -fx-border-insets: 20 15 15 15; -fx-background-color: white;");
        Label titleLabel = new Label(title);
        titleLabel.setStyle(
                "-fx-padding: 0px 5px 0px 5px;" +
                        "-fx-font-weight: bold;" +
                        "-fx-translate-y: " + (-Y_OFFSET - 10) +
                        "; -fx-background-color: white;"
        );
        StackPane.setAlignment(titleLabel, Pos.TOP_LEFT);
        setPadding(new Insets(Y_OFFSET, 15, 15, Y_OFFSET));
        getChildren().addAll(titleLabel, content);
    }
}

public class kalkulator extends Application {
    @Override
    public void start(Stage stage) throws IOException {
        //metoda obliczen
        ToggleGroup metodaObliczen = new ToggleGroup();
        RadioButton netto = new RadioButton("Od netto do brutto");
        netto.setToggleGroup(metodaObliczen);
        RadioButton brutto = new RadioButton("Od brutto do netto");
        brutto.setToggleGroup(metodaObliczen);
        RadioButton vat = new RadioButton("Dopasuj do kwoty VAT");
        vat.setToggleGroup(metodaObliczen);

        VBox metodaVBox = new VBox();
        metodaVBox.getChildren().addAll(netto,brutto,vat);
        BorderedTitledPane metodaBTP = new BorderedTitledPane("Metoda obliczen", metodaVBox);

        //dane
        Label wartoscLabel = new Label("Wartość bazowa:  ");
        TextField wartoscField = new TextField();
        Label vatStawkaLabel = new Label("Stawka VAT: ");
        ChoiceBox vatBox = new ChoiceBox();
        vatBox.getItems().addAll("23%", "8%", "5%", "0%");

        GridPane daneVBox = new GridPane();
        daneVBox.add(wartoscLabel,0,0);
        daneVBox.add(wartoscField,1,0);
        daneVBox.add(vatStawkaLabel,0,1);
        daneVBox.add(vatBox,1,1);
        BorderedTitledPane daneBTP = new BorderedTitledPane("Dane:", daneVBox);

        //wyniki
        Label nettoLabel= new Label("Netto:");
        Label vatLabel = new Label("VAT:");
        Label bruttoLabel = new Label("Brutto:");

        Label nettoWynikLabel = new Label("");
        Label vatWynikLabel = new Label("");
        Label bruttoWynikLabel = new Label("");

        VBox wynikiVBox = new VBox();
        wynikiVBox.getChildren().addAll(nettoLabel,vatLabel,bruttoLabel);

        VBox wynikVBox = new VBox();
        wynikVBox.getChildren().addAll(nettoWynikLabel,vatWynikLabel,bruttoWynikLabel);

        BorderPane wynikHBox = new BorderPane();
        wynikHBox.setLeft(wynikiVBox);
        wynikHBox.setRight(wynikVBox);

        BorderedTitledPane wynikBTP = new BorderedTitledPane("Wyniki:",wynikHBox);

        //2 przyciski:
        Button obliczBtn = new Button("OBLICZ");
        //obliczanie:
        obliczBtn.addEventHandler(MouseEvent.MOUSE_CLICKED, (e)->{
            RadioButton selectedMetoda = (RadioButton) metodaObliczen.getSelectedToggle();
            String metodaValue;
            if (selectedMetoda == null){
                Alert alert = new Alert(Alert.AlertType.ERROR);
                alert.setContentText("NIE WYBRANO METODY!");
                alert.show();
            } else {
                //wartosc
                Double wartosc = Double.parseDouble(wartoscField.getText());
                //rodzaj konwersji
                metodaValue = selectedMetoda.getText();
                //vat
                String vatValue = vatBox.getValue().toString();
                if (vatValue.isEmpty()) { vatValue = "23%"; }
                vatValue = vatValue.substring(0,vatValue.length()-1);
                int vatIntValue = Integer.parseInt(vatValue);

                Double nettoVal;
                double vatVal;
                double bruttoVal;
                float mnoznik = (float) (1.0 + (vatIntValue*0.01));
                //netto do brutto
                if(metodaValue.equals("Od netto do brutto")){
                    nettoVal = wartosc;
                    bruttoVal = nettoVal * mnoznik;
                    vatVal = bruttoVal - nettoVal;
                } else if (metodaValue.equals("Od brutto do netto")) { //brutto do netto
                    bruttoVal = wartosc;
                    nettoVal = bruttoVal/mnoznik;
                    vatVal = bruttoVal - nettoVal;
                } else  { //dopasuj do kwoty VAT
                    vatVal = wartosc;
                    nettoVal = (wartosc*100)/vatIntValue;
                    bruttoVal = nettoVal * mnoznik;
                }
                //zaokraglenie do 2 miejsc po przecinku
                nettoVal = nettoVal*100;
                nettoVal = (double) Math.round(nettoVal);
                nettoVal = nettoVal / 100;
                bruttoVal = bruttoVal*100;
                bruttoVal = (double) Math.round(bruttoVal);
                bruttoVal = bruttoVal / 100;
                vatVal = vatVal*100;
                vatVal = (double) Math.round(vatVal);
                vatVal = vatVal / 100;
                //wyswietlanie
                nettoWynikLabel.setText(Double.toString(nettoVal));
                bruttoWynikLabel.setText(Double.toString(bruttoVal));
                vatWynikLabel.setText(Double.toString(vatVal) + " @ " + vatValue + "%");
            }
        });

        Button zamknijBtn = new Button("ZAMKNIJ");
        zamknijBtn.addEventHandler(MouseEvent.MOUSE_CLICKED, (e)->{
            stage.close();
        });
        BorderPane btnsGrid = new BorderPane();
        btnsGrid.setLeft(obliczBtn);
        btnsGrid.setRight(zamknijBtn);
        btnsGrid.setPadding(new Insets(0,15,0,15));

        VBox vBox = new VBox();
        vBox.setMinSize(300, 500);
        vBox.setPadding(new Insets(10, 10, 10, 10));
        vBox.setAlignment(Pos.CENTER);
        vBox.setStyle("-fx-background-color: white;");

        vBox.getChildren().addAll(metodaBTP,daneBTP,btnsGrid,wynikBTP);
        Scene scene = new Scene(vBox);
        stage.setTitle("Kalkulator VAT netto-brutto");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}