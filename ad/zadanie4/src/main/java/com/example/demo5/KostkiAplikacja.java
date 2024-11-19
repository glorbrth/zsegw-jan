package com.example.demo5;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Random;


public class KostkiAplikacja extends Application {
    GridPane gridPane = new GridPane();
    ScrollPane scrollPane = new ScrollPane();
    VBox vBox = new VBox();
    Integer suma = 0;

    public void pokazKostki(int liczbaKostek){
        HBox hBox = new HBox();
        if(liczbaKostek != -1){

            ArrayList<Integer>tablicaKostek = new ArrayList<>();
            ArrayList<Image>tablicaZdjec = new ArrayList<>();
            try {
                tablicaZdjec.add(new Image(new FileInputStream("src/main/resources/image/dice0.png")));
                tablicaZdjec.add(new Image(new FileInputStream("src/main/resources/image/dice1.png")));
                tablicaZdjec.add(new Image(new FileInputStream("src/main/resources/image/dice2.png")));
                tablicaZdjec.add(new Image(new FileInputStream("src/main/resources/image/dice3.png")));
                tablicaZdjec.add(new Image(new FileInputStream("src/main/resources/image/dice4.png")));
                tablicaZdjec.add(new Image(new FileInputStream("src/main/resources/image/dice5.png")));
            } catch (FileNotFoundException e) {
                throw new RuntimeException(e);
            }

            Random random = new Random();

            for(int i = 0; i<liczbaKostek; i++){
                int los = random.nextInt(6);
                los = los + 1;
                tablicaKostek.add(los);
                ImageView kostka = new ImageView(tablicaZdjec.get(los-1));
                kostka.setFitHeight(40);
                kostka.setFitWidth(40);
                hBox.getChildren().add(kostka);
            }

            Label pkt = new Label();
            pkt.setText(policzPunkty(tablicaKostek));
            pkt.setStyle("-fx-margin:0");
            pkt.setStyle("-fx-font-size:30px");

            suma += Integer.parseInt(policzPunkty(tablicaKostek));

            hBox.getChildren().add(pkt);

            vBox.getChildren().add(hBox);

            scrollPane.setContent(vBox);

        }
    }

    public String policzPunkty(ArrayList tablicaKostek){
        int punkty = 0;
        int[] powtorzenia = {0,0,0,0,0,0};

        for(int i = 0; i<tablicaKostek.size();i++){
            int liczba = (int) tablicaKostek.get(i);
            powtorzenia[liczba-1]++;
        }
        for(int i = 0; i<powtorzenia.length; i++){
            if(powtorzenia[i]>1){
                punkty += (i+1) * powtorzenia[i];
            }
        }
        String punktyString = Integer.toString(punkty);
        return punktyString;
    }



    @Override
    public void start(Stage stage) throws IOException {
        scrollPane.setPrefSize(500,500);
        scrollPane.setHbarPolicy(ScrollPane.ScrollBarPolicy.NEVER);
        scrollPane.setVbarPolicy(ScrollPane.ScrollBarPolicy.ALWAYS);
        Label sumaLabel = new Label(suma.toString());
        //podanie ilosci kosci
        final int[] liczbaKostek = new int[1];
        TextField liczbaKostekField = new TextField();
        liczbaKostekField.setPrefSize(500,10);
        Button liczbaKostekBtn = new Button("graj");
        liczbaKostekBtn.addEventHandler(MouseEvent.MOUSE_CLICKED, (e) -> {

            if(liczbaKostekField.getText().equals("")){
                liczbaKostekField.setText("0");
            }
            liczbaKostek[0] = Integer.parseInt(liczbaKostekField.getText());
            if (liczbaKostek[0] < 3 || liczbaKostek[0] > 10){
                Alert alert = new Alert(Alert.AlertType.INFORMATION);
                alert.setTitle("zla liczba kostek");
                alert.setContentText("liczba kostek powinna byc w zakresie 3-10");
                alert.show();
                liczbaKostek[0] = -1;
                System.out.println("err");
            } else {
                pokazKostki(liczbaKostek[0]);
            }
            sumaLabel.setText(suma.toString());
        });

        Button resetSuma = new Button("reset sumy");
        resetSuma.addEventHandler(MouseEvent.MOUSE_CLICKED, (e) -> {
            scrollPane.setContent(null);
            vBox.getChildren().clear();
            suma = 0;
            sumaLabel.setText(suma.toString());
        });

        Label textSuma = new Label("Łączna suma to: ");
        gridPane.add(liczbaKostekField,0,0);
        gridPane.add(liczbaKostekBtn,1,0);
        gridPane.add(resetSuma,2,0);
        gridPane.add(textSuma,3,0);
        gridPane.add(sumaLabel,4,0);
        gridPane.add(scrollPane,0,1);

        Scene scene = new Scene(gridPane, 800, 600);
        stage.setTitle("Hello!");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}