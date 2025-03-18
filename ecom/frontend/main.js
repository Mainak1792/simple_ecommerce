const BACKEND_URL = "http://localhost:5000"

async function initDB() {
  const resultElem = document.getElementById("initResult");
  try {
    const response = await fetch(`${BACKEND_URL}/init-db`);
    if (response.ok) {
      const text = await response.text();
      resultElem.textContent = text;
    } else {
      resultElem.textContent = "Error initializing DB";
    }
  } catch (err) {
    console.error(err);
    resultElem.textContent = "Error connecting to the backend";
  }
}

async function getProducts() {
  const productsList = document.getElementById("productsList");
  productsList.innerHTML = "Loading...";
  try {
    const response = await fetch(`${BACKEND_URL}/products`);
    if (!response.ok) {
      productsList.innerHTML = "Error fetching products";
      return;
    }
    const products = await response.json();
    if (!products.length) {
      productsList.innerHTML = "<p>No products found.</p>";
      return;
    }
    let html = "<ul>";
    for (let p of products) {
      html += `<li>ID: ${p.id}, Name: ${p.name}, Price: ${p.price}</li>`;
    }
    html += "</ul>";
    productsList.innerHTML = html;
  } catch (err) {
    console.error(err);
    productsList.innerHTML = "Error connecting to backend";
  }
}

async function addProduct() {
  const nameInput = document.getElementById("productName");
  const priceInput = document.getElementById("productPrice");
  const resultElem = document.getElementById("addResult");
  resultElem.textContent = "";

  const productData = {
    name: nameInput.value,
    price: priceInput.value
  };

  try {
    const response = await fetch(`${BACKEND_URL}/products`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(productData)
    });
    if (response.ok) {
      const createdProduct = await response.json();
      resultElem.textContent = `Product added: ID = ${createdProduct.id}, Name = ${createdProduct.name}, Price = ${createdProduct.price}`;
      nameInput.value = "";
      priceInput.value = "";
    } else {
      resultElem.textContent = "Error adding product";
    }
  } catch (err) {
    console.error(err);
    resultElem.textContent = "Error connecting to backend";
  }
}

async function deleteProduct() {
  const deleteIdInput = document.getElementById("deleteId");
  const resultElem = document.getElementById("deleteResult");
  resultElem.textContent = "";

  try {
    const response = await fetch(`${BACKEND_URL}/products/${deleteIdInput.value}`, {
      method: "DELETE"
    });
    if (response.ok) {
      const text = await response.text();
      resultElem.textContent = text;
      deleteIdInput.value = "";
    } else {
      resultElem.textContent = "Error deleting product";
    }
  } catch (err) {
    console.error(err);
    resultElem.textContent = "Error connecting to backend";
  }
}
