var formData = new FormData();
var uploadedImages = [];
var num = 0;
var count = 1;

function uploadImage() {
    const fileInput = document.getElementById("image-input");
    const file = fileInput.files[0];
    const product_id = document.getElementById("product-id").value;
    formData.append("images", file);
    formData.append("product_id", product_id);
    fetch("/upload_image", {
        method: "POST",
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            var imageURL = data.image_url;
            uploadedImages.push(imageURL);
            product_id.value = data.product_id;
            displayImages();
        })
        .catch((error) => console.error(error));
}

function displayImages() {
    var previewDiv = document.getElementById("div-order-img");
    var images = document.querySelectorAll("img");
    var numImages = images.length;
    // Hide all the img
    images.forEach((img) => {
        img.style.display = "none";
    });
    // Create img uploaded
    var image = document.createElement("img");
    // img url
    image.src = uploadedImages[num];
    num += 1;
    image.className = "img-thumbnail";
    image.id = "index" + numImages.toString();
    // Show img uploaded
    image.style.display = "block";
    // Set position of count
    count = numImages;
    // Uploaded image at last position, so next should be disabled, and prev be able.
    document.querySelector("#next-image").disabled = true;
    document.querySelector("#prev-image").disabled = false;
    // Add uplaoded image to Img View Area
    previewDiv.appendChild(image);
}

function toggleImage(action) {
    const images = document.querySelectorAll(".img-thumbnail");

    images.forEach((img) => {
        img.style.display = "none";
    });

    // Show/Hide image with toggle buttons 'Prev' and 'Next'
    if (action == "prev") {
        count = count - 1;
        image = document.querySelector(`#index${count}`);
    } else if (action == "next") {
        count = count + 1;
        image = document.querySelector(`#index${count}`);
    }
    image.style.display = "block";

    // Disabled 'Prev' when out of range
    const btnPrev = document.querySelector("#prev-image");
    if (count <= 1) {
        btnPrev.disabled = true;
    } else {
        btnPrev.disabled = false;
    }

    // Disabled 'Next' when out of range
    const btnNext = document.querySelector("#next-image");
    if (count >= images.length) {
        btnNext.disabled = true;
    } else {
        btnNext.disabled = false;
    }
}

function updateSubCategories() {
    const typeSelect = document.getElementById("type-category").value;

    fetch(`/category/type/${typeSelect}`, {
        method: "GET",
    })
        .then((response) => response.json())
        .then((result) => {
            console.log(result);
            const subCategorySelect = document.getElementById("sub-category");
            // Remove existing sub category options
            subCategorySelect.innerHTML =
                "<option selected>Sub Category</option>";
            // Add New options based on type categories selected
            result.categories.forEach((category) => {
                const option = document.createElement("option");
                option.text = category.title;
                subCategorySelect.append(option);
            });
            // Show subCategory list
            subCategorySelect.style.display = "block";
        });
}

document.addEventListener("DOMContentLoaded", () => {
    // Show first image of product
    if (document.querySelector("#index1")) {
        document.querySelector("#index1").style.display = "block";
    }
    const images = document.querySelectorAll(".img-thumbnail");

    // Prev disabled initially.
    const btnPrev = document.querySelector("#prev-image");
    if (count <= 1) {
        btnPrev.disabled = true;
    } else {
        btnPrev.disabled = false;
    }
    // Next disabled initially if 1 image only.
    const btnNext = document.querySelector("#next-image");
    if (count >= images.length) {
        btnNext.disabled = true;
    } else {
        btnNext.disabled = false;
    }
});
