document.addEventListener("DOMContentLoaded", function () {
    document
        .querySelector("#btn-edit")
        .addEventListener("click", () => settings_view(event));
});

function settings_view(event) {
    event.preventDefault();
    // Settings view before clicking edit
    let username = document.querySelector("#username");
    let phone = document.querySelector("#phone");
    let address = document.querySelector("#address");
    username.disabled = false;
    phone.disabled = false;
    address.disabled = false;

    // Click and Hide Edit button
    let btnE = document.querySelector("#btn-edit");
    btnE.style.display = "none";
    // Prevent it from being clicked by 'Enter'
    btnE.disabled = true;

    // Create save button
    const btnS = document.createElement("button");
    btnS.textContent = "Save";
    btnS.id = "btn-save";
    btnS.className = "btn btn-primary";
    document.querySelector("#settings-form").append(btnS);

    // After click Save
    btnS.addEventListener("click", (e) => {
        e.preventDefault();
        // constraint phone number
        if (phone.value.length < 11 || phone.value.length > 12) {
            alert(
                "Invalid Phone Number: Phone number must be between 11 and 12 digits."
            );
            return false;
        }
        if (phone.value[0] !== "6" || phone.value[1] !== "0") {
            alert("Phone number must start with 60.");
            return false;
        }
        // constraint username with alphabets and numbers only
        const regex = /^[A-Za-z0-9]{6,}$/;
        if (!regex.test(username.value)) {
            alert(
                "Username must contain at least 6 characters, consisting of upper or lower case letters or numbers, and no punctuation"
            );

            username.value = "";
            return false;
        }

        // Save edited settings data
        edit_settings();
        // Remove Save Button
        btnS.remove();
        // Show edit button
        btnE.disabled = false;
        btnE.style.display = "block";

        document.querySelector("#username").disabled = true;
        document.querySelector("#phone").disabled = true;
        document.querySelector("#address").disabled = true;

        // Save successful message
        alert("Save succesfully.");
    });
}

function edit_settings() {
    // The settings the user edited
    const username = document.querySelector("#username").value;
    const phone = document.querySelector("#phone").value;
    const address = document.querySelector("#address").value;

    fetch("/settings/edit", {
        method: "POST",
        body: JSON.stringify({
            username: username,
            phone: phone,
            address: address,
        }),
    })
        .then((response) => response.json())
        .then((result) => {
            console.log(result);
            if (result.error === undefined) {
                console.log("yesssss");
            }
        });
}
