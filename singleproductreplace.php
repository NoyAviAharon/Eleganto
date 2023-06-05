<?php
$server_name = "localhost:3306";
$user_name = "korenta_Elega1";
$password = "123456";
$database_name = "korenta_DB1";
$conn = new mysqli($server_name, $user_name, $password, $database_name);
if ($conn->connect_error) {
   die("Connection failed: " . $conn->connect_error);
}

// Retrieve the product ID from the request parameters
$productId = $_GET['data-product-id'];


// Prepare the SQL query
$query = "SELECT * FROM products WHERE id = '$productId'";

// Execute the query using the database connection
$result = $conn->query($query);

// Check if the query execution was successful
if (!$result) {
   die('Query execution failed: ' . $conn->error);
}

// Process the query result and fetch the product information
$productInfo = $result->fetch_assoc();
$productName = $productInfo['name'];
$productPrice = $productInfo['base_price'];
$productImageURL = $productInfo['main_image_path'];
$productImageURL2 = $productInfo['image_path_2'];
$productImageURL3 = $productInfo['image_path_3'];
$productImageURL4 = $productInfo['image_path_4'];
$productImageURL5 = $productInfo['image_path_5'];
$productImageURL6 = $productInfo['image_path_6'];



// Read the singleproduct.html file
$htmlContent = file_get_contents('singleproduct.html');


// Replace the placeholder values with the retrieved product information
$htmlContent = str_replace('single product', $productName, $htmlContent);
$htmlContent = str_replace('productName', $productName, $htmlContent);
$htmlContent = str_replace('basePrice', $productPrice, $htmlContent);
$htmlContent = str_replace('SIMONA', $productName, $htmlContent);

$htmlContent = str_replace('img/img-products/SIMONA-RED.png', $productImageURL, $htmlContent);
$htmlContent = str_replace('img/img-products/SIMONA-WHITE.png', $productImageURL2, $htmlContent);
$htmlContent = str_replace('img/img-products/SIMONA-BLUE.png', $productImageURL3, $htmlContent);
$htmlContent = str_replace('img/img-products/SIMONA-BLACK.png', $productImageURL4, $htmlContent);
$htmlContent = str_replace('img/img-products/SIMONA-BROWN.png', $productImageURL5, $htmlContent);
$htmlContent = str_replace('img/img-products/SIMONA-360.png', $productImageURL6, $htmlContent);





$htmlContent = str_replace('product_name_to_qr', $productName, $htmlContent);
// Send the modified HTML as the response
header('Content-Type: text/html');
echo $htmlContent;




$conn->close();
?>
