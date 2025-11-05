package com.example.szyfr;

import javafx.application.Application;
import javafx.collections.ObservableList;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.FlowPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.Flow;
import java.util.stream.Collectors;

public class HelloApplication extends Application {
    public static List<String> readFile(String filePath) throws IOException {
        Path path = Paths.get(filePath);
        return Files.readAllLines(path);
    }

    public static void writeFile(String filePath, List<String> lines) throws IOException {
        Path path = Paths.get(filePath);
        Files.write(path, lines);
    }

    public String cipher(String text, int offset) {
        ArrayList<String> alfabet = new ArrayList<>();
        alfabet.add("a");alfabet.add("b");alfabet.add("c");alfabet.add("d");
        alfabet.add("e");alfabet.add("f");alfabet.add("g");alfabet.add("h");
        alfabet.add("i");alfabet.add("j");alfabet.add("k");alfabet.add("l");
        alfabet.add("m");alfabet.add("n");alfabet.add("o");alfabet.add("p");
        alfabet.add("q");alfabet.add("r");alfabet.add("s");alfabet.add("t");
        alfabet.add("u");alfabet.add("v");alfabet.add("w");alfabet.add("x");
        alfabet.add("y");alfabet.add("z");

        text = text.toLowerCase();

        offset = offset%26;

        StringBuilder result = new StringBuilder();

        for(int i = 0; i<text.length(); i++){
           char character = text.charAt(i);
           int ascii = (int) character;
           int asciiLetter;

           if(ascii + offset > 122) {
                asciiLetter = ascii + offset - 26;
           } else if (ascii + offset < 97) {
               asciiLetter = ascii + offset + 26;
           } else {
               asciiLetter = ascii + offset;
           }

           char newChar = (char) asciiLetter;
           result.append(newChar);
        }

        System.out.println(String.valueOf(result));
        return String.valueOf(result);
    }

    @Override
    public void start(Stage stage) throws IOException {

        Label sciezkaLabel = new Label("Ścieżka do odczytu");
        TextField sciezkaField = new TextField();

        FlowPane sciezka = new FlowPane();
        sciezka.getChildren().addAll(sciezkaLabel,sciezkaField);

        Label kluczLabel = new Label("Klucz szyfrowania");
        TextField kluczField = new TextField();

        FlowPane klucz = new FlowPane();
        klucz.getChildren().addAll(kluczLabel,kluczField);

        Button btnOdczyt = new Button("Odczytaj");
        //handler is near-end

        TextArea odczytOutput = new TextArea();
        odczytOutput.setEditable(true);
        odczytOutput.setPrefHeight(100);

        Button btnZapis = new Button("Zapisz");


        btnOdczyt.addEventHandler(MouseEvent.MOUSE_CLICKED, (mouseEvent -> {
            try {
                Integer szyfr = Integer.parseInt(kluczField.getText());
                odczytOutput.setText("");
                List<String> output = readFile(sciezkaField.getText());
                for(int i = 0; i<output.size();i++){
                    odczytOutput.appendText(cipher(output.get(i),-(szyfr) ) + "\n");
                }
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }));

        btnZapis.addEventHandler(MouseEvent.MOUSE_CLICKED, mouseEvent -> {
            try {
                Integer szyfr = Integer.parseInt(kluczField.getText());
                List<String> content = odczytOutput.getText().lines().collect(Collectors.toList());

                for(int i = 0; i<content.size(); i++){
                    content.set(i, cipher(content.get(i),szyfr));
                }

                writeFile(sciezkaField.getText(),content);

                System.out.println(content);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        });

        VBox vBox = new VBox();

        vBox.getChildren().addAll(sciezka, klucz, btnOdczyt, odczytOutput, btnZapis);


        Scene scene = new Scene(vBox, 320, 240);
        stage.setTitle("edytor tekstu");
        stage.setScene(scene);
        stage.show();

    }

    public static void main(String[] args) {
        launch();
    }
}