module com.example.szyfr {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.example.szyfr to javafx.fxml;
    exports com.example.szyfr;
}