package com.example.formpliki;

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

    @Override
    public void start(Stage stage) throws IOException {



        Label sciezkaLabel = new Label("Ścieżka do odczytu");
        TextField sciezkaField = new TextField();

        FlowPane sciezka = new FlowPane();
        sciezka.getChildren().addAll(sciezkaLabel,sciezkaField);

        Button btnOdczyt = new Button("Odczytaj");
        //handler is near-end

        TextArea odczytOutput = new TextArea();
        odczytOutput.setEditable(true);
        odczytOutput.setPrefHeight(100);

        Button btnZapis = new Button("Zapisz");


        btnOdczyt.addEventHandler(MouseEvent.MOUSE_CLICKED, (mouseEvent -> {
            try {
                odczytOutput.setText("");
                List<String> output = readFile(sciezkaField.getText());
                for(int i = 0; i<output.size();i++){
                    odczytOutput.appendText(output.get(i) + "\n");
                }
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }));

        btnZapis.addEventHandler(MouseEvent.MOUSE_CLICKED, mouseEvent -> {
            try {
                List<String> content = odczytOutput.getText().lines().collect(Collectors.toList());
                writeFile(sciezkaField.getText(),content);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        });

        VBox vBox = new VBox();

        vBox.getChildren().addAll(sciezka, btnOdczyt, odczytOutput, btnZapis);


        Scene scene = new Scene(vBox, 320, 240);
        stage.setTitle("edytor tekstu");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}