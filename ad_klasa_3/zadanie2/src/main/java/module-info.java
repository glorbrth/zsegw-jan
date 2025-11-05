module com.example.zadanie2 {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.example.zadanie2 to javafx.fxml;
    exports com.example.zadanie2;
}