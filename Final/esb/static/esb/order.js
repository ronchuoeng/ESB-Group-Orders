document.addEventListener("DOMContentLoaded", function () {
    const orderNo = document.querySelector("#order-no").innerHTML;

    const formJoin = document.querySelector("#form-join");
    formJoin.addEventListener("submit", (event) => {
        event.preventDefault();

        const confirmed = window.confirm(
            "Are you sure you want to join/edit this Order?"
        );

        if (confirmed) {
            formJoin.submit();
        }
    });
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
            if (data.total_quantity >= data.target_quantity) {
                orderDiv.style.backgroundColor = "rgba(121, 250, 121, 0.767)";
            } else {
                orderDiv.style.backgroundColor = "rgba(170, 170, 231, 0.632)";
            }
        })
        .catch((error) => {
            console.log(error);
        });
}
