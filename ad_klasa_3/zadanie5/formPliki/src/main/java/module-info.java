module com.example.formpliki {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.example.formpliki to javafx.fxml;
    exports com.example.formpliki;
}