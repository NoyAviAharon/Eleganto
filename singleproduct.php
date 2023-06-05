<?php
session_start();

$server_name = "localhost:3306";
$user_name = "korenta_Elega1";
$password = "123456";
$database_name = "korenta_DB1";
$conn = new mysqli($server_name, $user_name, $password, $database_name);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$Name = $_POST["name"];
$Color = $_POST["color"];
$Width = $_POST["width"];
$Height = $_POST["height"];
$Depth = $_POST["depth"];
$Price = $_POST["price"];
$Quantity = $_POST["quantity"];
$TotalPrice = $_POST["total_price"];

$product = array(
    "name" => $Name,
    "color" => $Color,
    "width" => $Width,
    "height" => $Height,
    "depth" => $Depth,
    "price" => $Price,
    "quantity" => $Quantity,
    "total_price" => $TotalPrice
);

if(empty($_SESSION["cart"])) {
    $_SESSION["cart"] = array($product);
} else {
    array_push($_SESSION["cart"], $product);
}

header("Location: store.php?success=1");
exit();
?>
