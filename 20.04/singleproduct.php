<?php
$server_name = "localhost:3306";
$user_name = "korenta_Elega1";
$password = "123456";
$database_name = "korenta_DB1";
$conn = new mysqli($server_name, $user_name, $password, $database_name);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$Code = $_POST["code"];
$Name = $_POST["name"];
$Color = $_POST["color"];
$Width = $_POST["width"];
$Height = $_POST["height"];
$Depth = $_POST["depth"];
$Price = $_POST["price"];
$Quantity = $_POST["quantity"];
$TotalPrice = $_POST["quantity"] * $_POST["price"];

$query = "INSERT INTO cart (code, name, color, width, height, depth, price, quantity, total_price) 
          VALUES ('$Code', '$Name', '$Color', '$Width', '$Height', '$Depth', '$Price', '$Quantity', '$TotalPrice')";

if ($conn->query($query) === FALSE) {
    echo "Can not add new product. Error is: " . $conn->error;
    exit();
}

echo "Thank you for your purchase!";
?>
