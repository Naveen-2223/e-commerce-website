// js/cart.js

fetch("http://localhost:5000/api/cart")
  .then(res => res.json())
  .then(items => {
    const cartDiv = document.getElementById("cart-items");
    if (items.length === 0) {
      cartDiv.innerHTML = "<p>Your cart is empty.</p>";
      return;
    }

    items.forEach(item => {
      const div = document.createElement("div");
      div.className = "product";
      div.innerHTML = `
        <h3>${item.name} - ₹${item.price}</h3>
        <p>${item.description}</p>
        <img src="${item.image_url || 'https://via.placeholder.com/100'}" width="100">
      `;
      cartDiv.appendChild(div);
    });
  })
  .catch(err => {
    console.error("Error loading cart:", err);
  });

function clearCart() {
  fetch("http://localhost:5000/api/clear_cart")
    .then(() => {
      alert("Cart cleared!");
      location.reload();
    });
}
