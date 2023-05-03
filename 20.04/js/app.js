const productImage = document.querySelector('.single-product-mg-container img');
const colorLinks = document.querySelectorAll('.products-color');
let selectedColor = '';

colorLinks.forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    const color = link.classList[2].split('-')[2];
    selectedColor = setColor(color);
    const newSrc = `img/img-products/product-1-${color}.png`;
    productImage.setAttribute('src', newSrc);

    // Add the selected-color class to the clicked button
    colorLinks.forEach(link => link.classList.remove('selected-color'));
    link.classList.add('selected-color');
  });
});

function setColor(color) {
  selectedColor = color;
  console.log(selectedColor);
  return selectedColor;
}

var qtyEl = document.getElementById("qty");
var qty = parseInt(qtyEl.innerHTML);

function increaseQty() {
  qty++;
  qtyEl.innerHTML = qty;
}

function decreaseQty() {
  if (qty > 1) {
    qty--;
    qtyEl.innerHTML = qty;
  }
}


function checkValues() {
  // get the size dimensions
  const widthInput = document.getElementById("width");
  const heightInput = document.getElementById("height");
  const depthInput = document.getElementById("depth");
  const width = parseInt(widthInput.value);
  const height = parseInt(heightInput.value);
  const depth = parseInt(depthInput.value);

  // check if any dimension is over 100
  if (width > 350 || height > 100 || depth > 350 || isNaN(width) || isNaN(height) || isNaN(depth)) {
    // show an error message
    alert("Values cannot be greater than max value that is written and please check your input is numbers only.");
  } else {
    // calculate the price per CM and change the price
    calculatePrice();
    // add the cart
    addToCart();
    // add the product to the cart
    alert("Product added to cart.");
    // reset the form
    document.querySelector("form").reset();
  }

}

function calculatePrice() {
  // get the size dimensions
  const widthInput = document.getElementById("width");
  const heightInput = document.getElementById("height");
  const depthInput = document.getElementById("depth");
  const width = parseInt(widthInput.value);
  const height = parseInt(heightInput.value);
  const depth = parseInt(depthInput.value);

  // calculate the price
  const basePrice = 200;
  const widthPrice = Math.max(0, width - 160) / 10 * 5;
  const heightPrice = Math.max(0, height - 80) / 10 * 5;
  const depthPrice = Math.max(0, depth - 80) / 10 * 5;
  const total = basePrice + widthPrice + heightPrice + depthPrice;

  // output the price to the website
  const priceElement = document.getElementById("product-price");
  priceElement.innerHTML = "$" + total.toFixed(2);
}


function addToCart() {


  function generateCode(length) {
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
  }

  // get the product details from the page
  var productName = document.getElementById('product-name').textContent;
  var productPrice = document.getElementById('product-price').textContent;
  var productQty = document.getElementById('qty').textContent;
  var productWidth = document.getElementById('width').value;
  var productHeight = document.getElementById('height').value;
  var productDepth = document.getElementById('depth').value;
  var productColor = selectedColor;

  // extract only the "200" from the product price
  var priceNumber = parseFloat(productPrice.substring(1));

  // create a new cart item object
  var cartItem = {
    name: productName,
    code: generateCode(8),
    price: productPrice,
    quantity: productQty,
    color: productColor,
    width: productWidth,
    height: productHeight,
    depth: productDepth,
    totalPrice: "$" + (priceNumber * parseInt(productQty)).toFixed(2)
  };
  console.log(cartItem);

  // update the cart numbers
  cartNumbers(cartItem);

  function cartNumbers(cartItem) {
    var productNumbers = localStorage.getItem('cartNumbers');

    if (productNumbers) {
      localStorage.setItem('cartNumbers', parseInt(productNumbers) + parseInt(cartItem.quantity));
      document.querySelector('.cart-items').textContent = parseInt(productNumbers) + parseInt(cartItem.quantity);
    } else {
      localStorage.setItem('cartNumbers', cartItem.quantity);
      document.querySelector('.cart-items').textContent = cartItem.quantity;
    }
  }

  setItems(cartItem);

  function setItems(cartItem) {
    let cartItems = localStorage.getItem('productsInCart');
    cartItems = JSON.parse(cartItems);

    if (cartItems != null) {
      cartItems = {
        ...cartItems,
        [cartItem.code]: cartItem
      };
    } else {
      cartItems = {
        [cartItem.code]: cartItem
      };
    }

    localStorage.setItem('productsInCart', JSON.stringify(cartItems));


    const myList = [];


    myList.push(cartItem); // add the object to the list


    // Log the updated list
    console.log(myList);
  }



  function setItems(cartItem) {
  // ...

  const tableBody = document.querySelector('.products');

  // Create a new table row element
  const newRow = document.createElement('tr');

  // Append new table data elements to the row element
  const codeCell = document.createElement('td');
  codeCell.textContent = cartItem.code;
  newRow.appendChild(codeCell);

  const nameCell = document.createElement('td');
  nameCell.textContent = cartItem.name;
  newRow.appendChild(nameCell);

  const colorCell = document.createElement('td');
  colorCell.textContent = cartItem.color;
  newRow.appendChild(colorCell);

  const widthCell = document.createElement('td');
  widthCell.textContent = cartItem.width;
  newRow.appendChild(widthCell);

  const heightCell = document.createElement('td');
  heightCell.textContent = cartItem.height;
  newRow.appendChild(heightCell);

  const depthCell = document.createElement('td');
  depthCell.textContent = cartItem.depth;
  newRow.appendChild(depthCell);

  const priceCell = document.createElement('td');
  priceCell.textContent = cartItem.price;
  newRow.appendChild(priceCell);

  const qtyCell = document.createElement('td');
  qtyCell.textContent = cartItem.quantity;
  newRow.appendChild(qtyCell);

  const totalPriceCell = document.createElement('td');
  totalPriceCell.textContent = cartItem.totalPrice;
  newRow.appendChild(totalPriceCell);

  // Append the new row element to the table body
  tableBody.appendChild(newRow);
}


}


function onLoadcartNumbers() {

  let productNumbers = localStorage.getItem('cartNumbers');

  if (productNumbers) {
    document.querySelector('.cart-items').textContent = productNumbers;

  }
}

onLoadcartNumbers()


function toggleColor(button) {
  // remove the 'active' class from all buttons
  let buttons = document.querySelectorAll('.products-color');
  for (let i = 0; i < buttons.length; i++) {
    buttons[i].classList.remove('active');
  }
  
  // add the 'active' class to the clicked button
  button.classList.add('active');
}


function openWindow() {
  var newWindow = window.open("", "", "width=800,height=500,top=50,left=50");
  newWindow.document.write('<html><head><title>3D Simulation View</title><link rel="stylesheet" type="text/css" href="css/qrcode.css"></head><body>');
  newWindow.document.write('<div class="logo-img">');
  newWindow.document.write('<img src="img/logo.png" alt="Logo">');
  newWindow.document.write('</div>');
  newWindow.document.write('<div class="container">');
  newWindow.document.write('<div class="text">');
  newWindow.document.write('<p>To view a 3D & AR simulation:</p>');
  newWindow.document.write('<ol>');
  newWindow.document.write('<li>Scan the QR code with your mobile device</li><br>');
  newWindow.document.write('<li>Rotate the product that appears on the screen with your finger to view in 3D.</li><br>');
  newWindow.document.write('<li>To view augmented reality (AR) through your camera - click "View In AR" on the top right.</li>');
  newWindow.document.write('</ol>');
  newWindow.document.write('</div>');
  newWindow.document.write('<div class="img-container">');
  newWindow.document.write('<img src="py/img-QRcode/qrcode_595dd625-64e1-4b87-9847-dadd1a1f18bf.png" alt="QR code">');
  newWindow.document.write('</div>');
  newWindow.document.write('</div>');
  newWindow.document.write('</body></html>');
}
