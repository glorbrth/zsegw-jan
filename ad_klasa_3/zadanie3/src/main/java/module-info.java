module com.example.zadanie3 {
    requires javafx.controls;
    requires javafx.fxml;
    requires java.desktop;

    opens com.example.zadanie3 to javafx.fxml;
    exports com.example.zadanie3;
}