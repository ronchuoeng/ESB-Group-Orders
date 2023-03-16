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
    const inputCusQuantity = document.getElementById(
        `input-cus${cus_order_id}`
    );
    const aTagEdit = document.getElementById(`edit-cus${cus_order_id}`);
    const btnSave = document.getElementById(`save${cus_order_id}`);

    // Hide and show the edit & save etc.
    if (quantity.style.display != "none") {
        quantity.style.display = "none";
        aTagEdit.style.display = "none";
        inputCusQuantity.style.display = "block";
        btnSave.style.display = "block";
    } else if (quantity.style.display == "none") {
        quantity.style.display = "block";
        aTagEdit.style.display = "block";
        inputCusQuantity.style.display = "none";
        btnSave.style.display = "none";
    }
}

// Enter to save after edit quantity
function saveOnEnter(event, order_id, type) {
    if (event.keyCode == 13 && type == "cus") {
        // edit cus input
        saveEditCusOrder(order_id);
    } else if (event.keyCode == 13 && type == "p_order") {
        // edit order input
        saveEditPurchaseOrder(order_id);
    }
}

function saveEditCusOrder(cus_order_id) {
    // Confirm
    const confirmed = confirm("Are you sure you want to save the edit?");

    if (confirmed) {
        const edited_cus_order_quantity = document.querySelector(
            `#input-cus${cus_order_id}`
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

function deletePurchaseOrder(p_order_id) {
    // Confirm
    const confirmed = confirm(
        "Are you sure you want to delete this purchase order?"
    );
    if (confirmed) {
        // Double Confirm
        const doubleConfirmed = confirm(
            "Warning: Deleting this purchase order will also delete all orders of the associated orderers. Are you sure you want to proceed with the deletion?"
        );
        if (doubleConfirmed) {
            fetch("/delete_purchase_order", {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    p_order_id: p_order_id,
                }),
            })
                .then((response) => response.json())
                .then((result) => {
                    if (result.message) {
                        console.log(result.message);
                        window.location.href = document.referrer;
                    }
                });
        }
    }
}

function editPurchaseOrder() {
    const inputOrderQuantity = document.getElementById("input-target-quantity");
    const inputOrderDateTime = document.getElementById(
        "input-expiration-datetime"
    );
    const aTagEdit = document.getElementById("edit-p-order");
    const btnSave = document.getElementById("save-edit-order");

    // Hide and show the edit & save etc.
    if (inputOrderQuantity.style.display == "none") {
        aTagEdit.style.display = "none";
        inputOrderQuantity.style.display = "block";
        inputOrderDateTime.style.display = "block";
        btnSave.style.display = "block";
    } else if (inputOrderQuantity.style.display == "block") {
        aTagEdit.style.display = "block";
        inputOrderQuantity.style.display = "none";
        inputOrderDateTime.style.display = "none";
        btnSave.style.display = "none";
    }
}

function saveEditPurchaseOrder(p_order_id) {
    // Confirm
    const confirmed = confirm("Are you sure you want to save the edit?");

    if (confirmed) {
        const edited_target_quantity = document.getElementById(
            "input-target-quantity"
        ).value;
        const edited_expiration_datetime_input = document.getElementById(
            "input-expiration-datetime"
        );
        // DateTime format
        const edited_expiration_datetime = new Date(
            edited_expiration_datetime_input.value
        );
        const edited_expiration_datetime_string =
            edited_expiration_datetime.toISOString();

        fetch("/save_edit_p_order", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                p_order_id: p_order_id,
                edited_target_quantity: edited_target_quantity,
                edited_expiration_datetime: edited_expiration_datetime_string,
            }),
        })
            .then((response) => response.json())
            .then((result) => {
                if (result.message) {
                    console.log(result.message);
                }
                // Refresh edited target quantity
                const quantity = document.getElementById("target-quantity");
                quantity.innerHTML = edited_target_quantity;
                // Refresh edited expiration date
                const datetime = document.getElementById("date-time");
                datetime.innerHTML = new Date(
                    edited_expiration_datetime
                ).toLocaleString();
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
        editPurchaseOrder();
    }
}
