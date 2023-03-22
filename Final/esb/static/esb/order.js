document.addEventListener("DOMContentLoaded", function () {
    // Get the Order.ID
    const orderNo = document.querySelector("#order-no").innerHTML;
    // Get the Order form
    const formJoin = document.querySelector("#form-join");
    let confirmed;

    // Button click for Edit/Join Order
    const btnJoin = document.querySelector("#btn-join");
    if (btnJoin) {
        btnJoin.addEventListener("click", (event) => {
            confirmed = window.confirm(
                "Are you sure you want to join/edit the Order?"
            );
            if (!confirmed) {
                event.preventDefault();
            }
        });
    }
    // Button click for Delete Order
    const btnCancel = document.querySelector("#btn-cancel");
    if (btnCancel) {
        btnCancel.addEventListener("click", (event) => {
            confirmed = window.confirm(
                "Are you sure you want to cancel the Order?"
            );
            if (!confirmed) {
                event.preventDefault();
            }
        });
    }
    // refresh Ordered people every 10 seconds.
    setInterval(() => refreshOrder(orderNo), 10000);
});

function refreshOrder(order_id) {
    fetch(`/order/${order_id}/refresh`, {
        method: "GET",
    })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            // refresh target and total quantity display
            const orderPeople = document.querySelector("#span-target");
            orderPeople.innerHTML = `[${data.total_quantity}/${data.target_quantity}]`;

            // refresh backgroundColor
            const orderDiv = document.querySelector(".div-target");
            const orderStatus = document.querySelector("#order-status");
            if (data.total_quantity >= data.target_quantity) {
                orderDiv.style.backgroundColor = "rgba(121, 250, 121, 0.767)";
                orderStatus.style.backgroundColor =
                    "rgba(121, 250, 121, 0.767)";
            } else {
                orderDiv.style.backgroundColor = "rgba(170, 170, 231, 0.632)";
                orderStatus.style.backgroundColor =
                    "rgba(170, 170, 231, 0.632)";
            }
        })
        .catch((error) => {
            console.log(error);
        });
}
