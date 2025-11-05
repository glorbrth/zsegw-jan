module com.example.baza_uczen {
    requires javafx.controls;
    requires javafx.fxml;
    requires java.sql;
    requires mysql.connector.j;
    requires jdk.jsobject;


    opens com.example.baza_uczen to javafx.fxml;
    exports com.example.baza_uczen;
}