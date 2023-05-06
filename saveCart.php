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

$session_id = session_id();

if(isset($_POST['continue_payment'])) {
    foreach ($_SESSION['cart'] as $product) {
        $name = $product['name'];
        $color = $product['color'];
        $width = $product['width'];
        $height = $product['height'];
        $depth = $product['depth'];
        $price = $product['price'];
        $quantity = $product['quantity'];
        $total_price = $product['total_price'];

        $query = "INSERT INTO orders (session_id, name, color, width, height, depth, price, quantity, total_price) 
                  VALUES ('$session_id', '$name', '$color', '$width', '$height', '$depth', '$price', '$quantity', '$total_price')";

        if ($conn->query($query) === FALSE) {
            echo "Can not add new product. Error is: " . $conn->error;
            exit();
        }
    }

    session_destroy();
    header("Location: successPage.html?success=1");
    exit();
} else {
    echo "Invalid request";
    exit();
}
?>
