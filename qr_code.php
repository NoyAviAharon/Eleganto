<?php
$server_name = "localhost:3306";
$user_name = "korenta_Elega1";
$password = "123456";
$database_name = "korenta_DB1";
$prduct_name=$_GET["product_name"];


$conn = new mysqli($server_name, $user_name, $password, $database_name);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);}

$sql = "SELECT * FROM Model_link";
$result = mysqli_query($conn, $sql);
if (mysqli_num_rows($result) > 0) {
  while($row = mysqli_fetch_assoc($result)) {
    $link = $row["model_link"];
    $name = $row["model_name"];
    if ($name==$prduct_name){
      $image_url = "https://api.qrserver.com/v1/create-qr-code/?data=" . urlencode($link) . "&size=100x100";
    }

 
  }
} else {
  echo "0 results";}
mysqli_close($conn);
$data = array('image_url' => $image_url);
$json_string = json_encode($data);
header('Content-type: text/javascript');
echo $json_string;
?>