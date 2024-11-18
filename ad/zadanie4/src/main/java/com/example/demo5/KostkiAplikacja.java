package com.example.demo5;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.stage.Stage;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Random;


public class KostkiAplikacja extends Application {
    GridPane gridPane = new GridPane();

    public void pokazKostki(int liczbaKostek, int game){
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

            HBox hBox = new HBox();

            Random random = new Random();
            String tempTab = "";

            for(int i = 0; i<liczbaKostek; i++){
                int los = random.nextInt(6);
                los = los + 1;
                tablicaKostek.add(los);
                tempTab += los;
                ImageView kostka = new ImageView(tablicaZdjec.get(los-1));
                kostka.setFitHeight(20);
                kostka.setFitWidth(20);
                hBox.getChildren().add(kostka);
            }

            Label pkt = new Label();
            pkt.setText(policzPunkty(tablicaKostek));

            hBox.getChildren().add(pkt);

            gridPane.add(hBox,0,game);
            game++;
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
        final int[] game = {1};
        //podanie ilosci kosci
        final int[] liczbaKostek = new int[1];
        TextField liczbaKostekField = new TextField();
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
                pokazKostki(liczbaKostek[0], game[0]);
                game[0]++;
            }
        });

        Button wyjdzBtn = new Button("zakoncz");
        wyjdzBtn.addEventHandler(MouseEvent.MOUSE_CLICKED, (e) -> {
            ((Stage)(((Button)e.getSource()).getScene().getWindow())).close();
        });




        gridPane.add(liczbaKostekField,0,0);
        gridPane.add(liczbaKostekBtn,1,0);
        gridPane.add(wyjdzBtn,2,0);


        Scene scene = new Scene(gridPane, 320, 240);
        stage.setTitle("Hello!");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}