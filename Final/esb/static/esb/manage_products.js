document.addEventListener("DOMContentLoaded", function () {
    const containerD = document.querySelector(".container-description");
    const containerT = document.querySelector(".container-title");
    const containerB = document.querySelector(".container-body");
    const table = document.querySelector("table");

    // If screen smaller than 992px, description is too long for it,so we hide it
    if (window.innerWidth < 992) {
        const descriptionView = document.querySelectorAll(".p-description");
        descriptionView.forEach((view) => {
            view.style.display = "none";
            // Create Button for view description
            const btnView = document.createElement("button");
            btnView.innerHTML = "View Description";
            btnView.className = "btn btn-primary";

            btnView.onclick = () => {
                // Hide the table
                table.style.display = "none";
                // Show description in containerD div
                containerT.innerHTML = "<h4>Description</h4>";
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
            };
            view.parentElement.append(btnView);
        });
    }
});

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
