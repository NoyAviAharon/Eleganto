// get references to the plus and minus buttons
const plusBtn = document.querySelector('.plus-btn');
const minusBtn = document.querySelector('.minus-btn');

// add event listeners to the plus and minus buttons
plusBtn.addEventListener('click', addToCart);
minusBtn.addEventListener('click', removeFromCart);


function increaseQuantity(productID) {
  const quantityElement = document.getElementById(productID + '-quantity');
  let quantity = parseInt(quantityElement.innerText);
  quantity++;
  quantityElement.innerText = quantity;
}


// function to add an item to the cart
function addToCart() {
  // get the item ID from the button data attribute
  const itemId = plusBtn.dataset.itemId;
  
  // get the current quantity for this item
  let quantity = localStorage.getItem(itemId);
  
  // increment the quantity by 1
  quantity = parseInt(quantity) + 1;
  
  // update the quantity in local storage
  localStorage.setItem(itemId, quantity);
  
  // update the UI
  updateCart();
}

// function to remove an item from the cart
function removeFromCart() {
  // get the item ID from the button data attribute
  const itemId = minusBtn.dataset.itemId;
  
  // get the current quantity for this item
  let quantity = localStorage.getItem(itemId);
  
  // decrement the quantity by 1, but not below zero
  quantity = Math.max(parseInt(quantity) - 1, 0);
  
  // update the quantity in local storage
  localStorage.setItem(itemId, quantity);
  
  // update the UI
  updateCart();
}

// function to update the cart UI
function updateCart() {
  // get references to the sub total, tax, shipping, and order total fields
  const subTotal = document.querySelector('.sub-total');
  const tax = document.querySelector('.tax');
  const shipping = document.querySelector('.shipping');
  const orderTotal = document.querySelector('.order-total');
  
  // calculate the new values for the fields based on the quantities in local storage
  const totalQuantity = Object.values(localStorage).reduce((acc, val) => acc + parseInt(val), 0);
  const subTotalValue = totalQuantity * 100;
  const taxValue = subTotalValue * 0.1;
  const shippingValue = totalQuantity * 10;
  const orderTotalValue = subTotalValue + taxValue + shippingValue;
  
  // update the values in the UI
  subTotal.textContent = `$${subTotalValue.toFixed(2)}`;
  tax.textContent = `$${taxValue.toFixed(2)}`;
  shipping.textContent = `$${shippingValue.toFixed(2)}`;
  orderTotal.textContent = `$${orderTotalValue.toFixed(2)}`;
}
