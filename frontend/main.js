// Fetch and display products
fetch("http://localhost:5000/api/products")
  .then(res => res.json())
  .then(products => {
    const list = document.getElementById("product-list");

    if (!Array.isArray(products)) {
      list.innerHTML = "<p>⚠️ Failed to load products.</p>";
      return;
    }

    products.forEach(p => {
      const col = document.createElement("div");
      col.className = "col-md-4 mb-4";

      col.innerHTML = `
        <div class="card h-100 shadow-sm">
          <img src="${p.image_url}" class="card-img-top" alt="${p.name}" style="height: 150px; object-fit: contain;">
          <div class="card-body">
            <h5 class="card-title">${p.name}</h5>
            <p class="card-text">${p.description}</p>
            <h6 class="card-subtitle mb-2 text-muted">₹${p.price}</h6>
            <button class="btn btn-success" onclick="addToCart('${p._id}')">Add to Cart</button>
          </div>
        </div>
      `;
      list.appendChild(col);
    });
  })
  .catch(err => {
    console.error("❌ Failed to fetch products:", err);
    document.getElementById("product-list").innerHTML = "Error loading products.";
  });

function addToCart(id) {
  fetch(`http://localhost:5000/api/add_to_cart/${id}`).then(() => {
    alert("✅ Added to cart!");
  });
}
