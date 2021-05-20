var updateBtns = document.getElementsByClassName("update-basket");

for (var i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    console.log("productId:", productId, "action:", action);

    console.log("USER:", user);
    if (user == "AnonymousUser") {
      console.log("User is not suthenticated");
    } else {
      updateUserOrder(productId, action);
    }
  });
}
function updateUserOrder(productId, action) {
  console.log("User is authenticated");

  var url = "/update_product/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("data", data);
    });
}
