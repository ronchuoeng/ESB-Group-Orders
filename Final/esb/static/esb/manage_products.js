function viewDescription(product_id) {
    const containerD = document.querySelector(".container-description");
    const containerT = document.querySelector(".container-title");
    const containerB = document.querySelector(".container-body");
    const table = document.querySelector("table");
    const view = document.querySelector(`#p-description${product_id}`);
    const title = document.querySelector(`#p-title${product_id}`);

    // Hide the table
    table.style.display = "none";
    // Show description in containerD div
    containerT.innerHTML =
        "<h4>" + title.innerHTML + "</h4>" + "<h5>Description:</h5>";
    containerB.innerHTML = view.innerHTML;
    containerD.style.display = "block";

    // Create Button for go back
    const goBack = document.createElement("button");
    const divGoBack = document.createElement("div");
    // Button value and style
    goBack.innerHTML = "Back";
    goBack.className = "btn btn-primary";

    divGoBack.appendChild(goBack);
    containerD.appendChild(divGoBack);

    goBack.onclick = () => {
        // Hide containerD div
        containerB.innerHTML = "";
        containerD.style.display = "none";
        // Show the table
        table.style.display = "block";
        goBack.parentElement.removeChild(goBack);
    };
}

function deleteProduct(product_id) {
    // Confirm
    const confirmed = confirm("Are you sure you want to delete this product?");

    if (confirmed) {
        fetch(`/delete_product`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                product_id: product_id,
            }),
        })
            .then((response) => {
                console.log(response);
                return response.json();
            })
            .then((data) => {
                console.log(data);
                if (data.message) {
                    const tr = document.getElementById(`tr${product_id}`);
                    if (tr) {
                        tr.remove();
                    }
                } else {
                    alert(data.error);
                }
            });
    }
}

function activeProduct(product_id) {
    // Turn the status of product to Active/Inactive
    fetch(`/product/${product_id}/active`, {
        method: "PUT",
    }).then((response) => {
        if (response.status === 204) {
        }
    });
    const productStatus = document.getElementById(`order-${product_id}`);
    if (productStatus.innerHTML == "Active") {
        productStatus.innerHTML = "Inactive";
        productStatus.className = "text-danger";
    } else {
        productStatus.innerHTML = "Active";
        productStatus.className = "text-success";
    }
}

function editProduct(product_id) {}
