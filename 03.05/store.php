<?php
$server_name = "localhost:3306";
$user_name = "korenta_Elega1";
$password = "123456";
$database_name = "korenta_DB1";
$conn = new mysqli($server_name, $user_name, $password, $database_name);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$query = "SELECT * FROM cart";
$result = $conn->query($query);
?>

<html lang="en">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta http-equiv="X-UA-Compatible" content="ie=edge" />
  <!-- bootstrap css -->
  <link rel="stylesheet" href="css/bootstrap.min.css" />
  <!-- main css -->
  <link rel="stylesheet" href="css/main.css" />
  <!-- google fonts -->
  <link href="https://fonts.googleapis.com/css?family=Courgette" rel="stylesheet" />
  <script src="js/store.js"></script>
  <!-- font awesome -->
  <link rel="stylesheet" href="css/all.css" />
  <title>Eleganto</title>
  <style>
    
	
    table {
      border-collapse: separate;
      border-spacing: 0 10px;
    }

    th,
    td {
      border: 1px solid black;
      padding: 10px;
    }
  </style>
</head>

<body>
  <!--
      https://www.iconfinder.com/icons/185106/armchair_chair_streamline_icon
      Creative Commons (Attribution 3.0 Unported);
      https://www.iconfinder.com/webalys
    -->

  <header>
        <!--Navbar-->
	<nav class="navbar navbar-expand-lg navbar-light">
	  <!--
	  https://www.iconfinder.com/icons/185106/armchair_chair_streamline_icon
	  Creative Commons (Attribution 3.0 Unported);
	  https://www.iconfinder.com/webalys
	-->
	 <a href="index.html" class="navbar-brand">
		<img src="img/logo.png" alt="company logo" class="logo-img">
	 </a>
	 <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#myNavbar">
		<i class="fas fa-bars"></i>
	 </button>
	 <div class="collapse navbar-collapse" id="myNavbar">
		<ul class="navbar-nav mx-auto">
		  <li class="nav-item mx-2">
			<a href="index.html" class="nav-link">Home</a>
		  </li>
		  <li class="nav-item mx-2">
			<a href="products.html" class="nav-link">Products</a>
		  </li>
		  <li class="nav-item mx-2">
			<a href="singleproduct.html" class="nav-link">Single Product</a>
		  </li>
		  <li class="nav-item mx-2">
			<a href="store.html" class="nav-link">Store</a>
		  </li>
		</ul>
	 </div>
	 <div class="navbar-icons d-flex align-items-center">
		<!--Cart icon-->
		<a href="store.html" class="navbar-icon mx-2 navbar-cart-icon">
		  <div class="cart-items">0</div>
		  <i class="fas fa-shopping-cart"></i>
		</a>
		<!--End of Cart icon-->
	  </div>
	</nav>
	<!--End of Navbar-->


    <div class="banner-store d-flex align-items-center justify-content-center pl-3 pl-lg-5 text-center">
      <div>
        <h1 class="text-capitalize text-yellow text-slanted display-4">
          Eleganto
        </h1>
        <h1 class="text-capitalize font-weight-bold display-4">
          our store
        </h1>
      </div>
    </div>


  </header>
  <!--End of Header Section-->


	 <table>
        <thead>
            <tr>
                <th>Code</th>
                <th>Name</th>
                <th>Color</th>
                <th>Width</th>
                <th>Height</th>
                <th>Depth</th>
                <th>Price</th>
                <th>Quantity</th>
                <th>Total Price</th>
            </tr>
        </thead>
        <tbody>
            <?php while ($row = $result->fetch_assoc()): ?>
            <tr>
                <td><?php echo $row['code']; ?></td>
                <td><?php echo $row['name']; ?></td>
                <td><?php echo $row['color']; ?></td>
                <td><?php echo $row['width']; ?></td>
                <td><?php echo $row['height']; ?></td>
                <td><?php echo $row['depth']; ?></td>
                <td><?php echo $row['price']; ?></td>
                <td><?php echo $row['quantity']; ?></td>
                <td><?php echo $row['total_price']; ?></td>
            </tr>
            <?php endwhile; ?>
        </tbody>
    </table>


  <!--Skills Section-->
  <section class="skills py-5">
    <div class="container">
      <div class="row">
        <!--Single Skill-->
        <div class="col-10 mx-auto col-md-6 col-lg-4 d-flex my-3">
          <div class="skill-icon mr-3">
            <i class="fas fa-truck"></i>
          </div>
          <div class="skill-text">
            <h3 class="text-uppercase text-white">free shipping</h3>
            <p class="text-muted text-capitalize">
              Enjoy free shipping on all orders at Eleganto. No minimum purchase required.
            </p>
          </div>
        </div>
        <!--End of Single Skill-->
        <!--Single Skill-->
        <div class="col-10 mx-auto col-md-6 col-lg-4 d-flex my-3">
          <div class="skill-icon mr-3">
            <i class="fas fa-comment-dollar"></i>
          </div>
          <div class="skill-text">
            <h3 class="text-uppercase text-white">price promise</h3>
            <p class="text-muted text-capitalize">
              Eleganto offers a price promise - if you find a lower price on an identical item at another store, we'll match it.
            </p>
          </div>
        </div>
        <!--End of Single Skill-->
        <!--Single Skill-->
        <div class="col-10 mx-auto col-md-6 col-lg-4 d-flex my-3">
          <div class="skill-icon mr-3">
            <i class="fas fa-award"></i>
          </div>
          <div class="skill-text">
            <h3 class="text-uppercase text-white">lifetime warranty</h3>
            <p class="text-muted text-capitalize">
              Shop with confidence at Eleganto - we offer a lifetime warranty on all our products.
            </p>
          </div>
        </div>
        <!--End of Single Skill-->
      </div>
    </div>
  </section>
  <!--End of Skills Section-->

  <!--Footer Section-->
  <footer class="py-5 footer">
    <div class="container">
      <div class="row">
        <div class="col-10 mx-auto text-center">
          <h1 class="text-uppercase font-weight-bold text-yellow footer-title text-center d-inline-block">
            Eleganto
          </h1>
          <div class="footer-icons my-5 d-flex justify-content-center">
            <!--Single Icon-->
            <a href="https://www.facebook.com/profile.php?id=100075578007039&mibextid=LQQJ4d" class="footer-icon mx-2">
              <i class="fab fa-facebook"></i>
            </a>
            <!--End of Single Icon-->
            <!--Single Icon-->
            <a href="https://rb.gy/li3a7" class="footer-icon mx-2">
              <i class="fab fa-whatsapp"></i>
            </a>
            <!--End of Single Icon-->
            <!--Single Icon-->
            <a href="https://instagram.com/eleganto_homedecor?igshid=YmMyMTA2M2Y=" class="footer-icon mx-2">
              <i class="fab fa-instagram"></i>
            </a>
            <!--End of Single Icon-->
          </div>
          <!--End of Footer Icons-->
          <p class="text-muted text-capitalize w-75 mx-auto text-center">
            Design your dream furniture for your home with Eleganto!</br>
            With our augmented reality technology, you can see your custom designs come</br>
            to life right in your own private space through your phone screen.</br> Discover how our home products will look in your home before you make a purchase.
            Try it out now!
          </p>
          <div class="footer-contact mt-5 d-flex justify-content-around flex-wrap">
            <!--Single contact-->
            <div class="text-capitalize">
              <span class="footer-icon mr-2">
                <i class="fas fa-map"></i>
              </span>
              Havoda 65, Ashdod
            </div>
            <!--End of Single contact-->
            <!--Single contact-->
            <div class="text-capitalize">
              <span class="footer-icon mr-2">
                <i class="fas fa-phone"></i>
              </span>
              phone : 050-429-8614
            </div>
            <!--End of Single contact-->
            <!--Single contact-->
            <div class="text-capitalize">
              <span class="footer-icon mr-2">
                <i class="fas fa-envelope"></i>
              </span>
              email : elegantodesign1@gmail.com
            </div>
            <!--End of Single contact-->
          </div>
        </div>
      </div>
    </div>
  </footer>
  <!--End of Footer Section-->

  <!-- modal -->
  <div class="modal fade" id="productModal" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <!--modal header-->
        <div class="modal-header">
          <h5 class="modal-title text-capitalize">product info</h5>
          <button type="button" class="close" data-dismiss="modal">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <!--end of modal header-->

        <!--modal body -->
        <div class="modal-body">
          <div class="row">
            <div class="col text-center">
              <img src="img/img-products/product-1.png" class="img-fluid" alt="">
              <!--ratings-->
              <div class="ratings">
                <span class="rating-icon">
                  <i class="fas fa-star"></i>
                </span>
                <span class="rating-icon">
                  <i class="fas fa-star"></i>
                </span>
                <span class="rating-icon">
                  <i class="fas fa-star"></i>
                </span>
                <span class="rating-icon">
                  <i class="fas fa-star"></i>
                </span>
                <span class="rating-icon">
                  <i class="far fa-star"></i>
                </span>
                <span class="text-capitalize">(25 customer reviews</span>
              </div>
              <!--end of ratings-->
              <h2 class="text-uppercase my-2">
                premium office armchair
              </h2>
              <h2>$10.00 - $200.00</h2>
              <p class="lead text-muted">
                Lorem, ipsum dolor sit amet consectetur adipisicing elit. Pariatur, aliquam!
              </p>
              <!-- colors -->
              <h5 class="text-uppercase">
                colors :
                <span class="d-inline-block products-color products-color-black mr-2"></span>
                <span class="d-inline-block products-color products-color-red mr-2"></span>
                <span class="d-inline-block products-color products-color-blue mr-2"></span>
              </h5>
              <!-- end of colors -->

              <!--sizes-->
              <h5 class="text-uppercase">
                sizes :
                <span class="mx-2">xs</span>
                <span class="mx-2">sm</span>
                <span class="mx-2">md</span>
                <span class="mx-2">lg</span>
                <span class="mx-2">xl</span>
              </h5>
              <!--end of sizes-->
              <div class="d-flex flex-wrap">
                <!-- cart buttons -->
                <div class="d-flex my-2">
                  <span class="btn btn-black mx-1">-</span>
                  <span class="btn btn-black mx-1">4</span>
                  <span class="btn btn-black mx-1">+</span>
                </div>
                <button class="btn btn-black my-2 mx-2">
                  wishlist
                </button>
                <button class="btn btn-yellow my-2 mx-2">
                  add to cart
                </button>
              </div>
            </div>
          </div>
        </div>
        <!--end of modal body -->
        <div class="modal-footer">
          <button type="button" class="btn btn-danger" data-dismiss="modal">close modal</button>
        </div>
      </div>

    </div>
  </div>


  <div id="cart-items-container"></div>



  <!-- jquery -->


  <script>
	const cartItemsBody = document.getElementById('cart-items-body');
	const cartItems = JSON.parse(localStorage.getItem('cartItems'));

	for (let i = 0; i < cartItems.length; i++) {
	  const cartItem = cartItems[i];
	  const tr = document.createElement('tr');

	  const productNameTd = document.createElement('td');
	  productNameTd.textContent = cartItem.productName;
	  tr.appendChild(productNameTd);

	  const productPriceTd = document.createElement('td');
	  productPriceTd.textContent = cartItem.productPrice;
	  tr.appendChild(productPriceTd);

	  const productQuantityTd = document.createElement('td');
	  productQuantityTd.textContent = cartItem.productQuantity;
	  tr.appendChild(productQuantityTd);

	  const productSizeTd = document.createElement('td');
	  productSizeTd.textContent = cartItem.productSize;
	  tr.appendChild(productSizeTd);

	  cartItemsBody.appendChild(tr);
	}

  </script>



  <script src="js/jquery-3.3.1.min.js"></script>
  <!-- bootstrap js -->
  <script src="js/bootstrap.bundle.min.js"></script>
  <!-- script js -->
  <script src="js/app.js"></script>
</body>

</html>
