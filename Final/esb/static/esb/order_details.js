function deleteCusOrder(cus_order_id) {
    // Confirm
    const confirmed = confirm(
        "Are you sure you want to delete the customer's order?"
    );

    if (confirmed) {
        fetch(`/delete_cus_order`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                cus_order_id: cus_order_id,
            }),
        })
            .then((response) => {
                console.log(response);
                return response.json();
            })
            .then((data) => {
                console.log(data);
                const tr = document.getElementById(`tr${cus_order_id}`);
                if (tr) {
                    tr.remove();
                }
            });
    }
}

function editCusOrder(cus_order_id) {
    const quantity = document.getElementById(`sp${cus_order_id}`);
    const inputQuantity = document.getElementById(`input${cus_order_id}`);
    const aTagEdit = document.getElementById(`edit${cus_order_id}`);
    const btnSave = document.getElementById(`save${cus_order_id}`);

    // Hide and show the edit & save etc.
    if (quantity.style.display != "none") {
        quantity.style.display = "none";
        aTagEdit.style.display = "none";
        inputQuantity.style.display = "block";
        btnSave.style.display = "block";
    } else if (quantity.style.display == "none") {
        quantity.style.display = "block";
        aTagEdit.style.display = "block";
        inputQuantity.style.display = "none";
        btnSave.style.display = "none";
    }
}

// Enter to save after edit quantity
function saveOnEnter(event, cus_order_id) {
    if (event.keyCode == 13) {
        saveEditCusOrder(cus_order_id);
    }
}

function saveEditCusOrder(cus_order_id) {
    // Confirm
    const confirmed = confirm("Are you sure you want to save the edit?");

    if (confirmed) {
        const edited_cus_order_quantity = document.querySelector(
            `#input${cus_order_id}`
        ).value;

        fetch(`/save_edit_cus_order`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                cus_order_id: cus_order_id,
                edited_cus_order_quantity: edited_cus_order_quantity,
            }),
        })
            .then((response) => response.json())
            .then((result) => {
                if (result.message) {
                    console.log(result.message);
                }
                // Refresh edited quantity
                const quantity = document.getElementById(`sp${cus_order_id}`);
                quantity.innerHTML = edited_cus_order_quantity;
                // Refresh total quantity
                const totalQuantity = document.getElementById("total-quantity");
                totalQuantity.innerHTML = result.total_quantity;
                // Refresh order status
                const orderStatus = document.getElementById("order-status");

                if (result.reach_target) {
                    orderStatus.innerHTML = `<span class="text-success">In Progress</span>`;
                } else {
                    if (result.is_expired) {
                        orderStatus.innerHTML = `<span class="text-danger">Expired</span>`;
                    } else {
                        orderStatus.innerHTML = `Pending`;
                    }
                }
            })
            .catch((error) => console.error(error));

        // Hide & Show the edit & save etc.
        editCusOrder(cus_order_id);
    }
}
