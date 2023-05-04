<?php
$server_name = "localhost:3306";
$user_name = "korenta_Elega1";
$password = "123456";
$database_name = "korenta_DB1";
$conn = new mysqli($server_name, $user_name, $password, $database_name);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$Name = $_POST["name"];
$Email = $_POST["email"];
$Password = $_POST["password"];


$query = "INSERT INTO registration (name, email, password)
          VALUES ('$Name', '$Email', '$Password')";



if ($conn->query($query) === FALSE) {
    echo "Can not add new product. Error is: " . $conn->error;
    exit();
}

echo "Registration was successful, please proceed to the payment page.<br> <a href='paymentPage'>Click here to pay</a>";

?>
