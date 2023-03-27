var formData = new FormData(); // Create formdata fill by input of form in html
var uploadedImages = [];
var num = 0;
var count = 1;

document.addEventListener("DOMContentLoaded", () => {
    // Show first image of product
    if (document.querySelector("#index1")) {
        document.querySelector("#index1").style.display = "block";
        const btnDelete = document.querySelector("#index-delete1");
        if (btnDelete) {
            btnDelete.style.display = "block";
        }
    }
    const images = document.querySelectorAll(".img-thumbnail");

    // Prev disabled initially.
    const btnPrev = document.querySelector("#prev-image");
    if (btnPrev) {
        if (count <= 1) {
            btnPrev.disabled = true;
        } else {
            btnPrev.disabled = false;
        }
    }
    // Next disabled initially if 1 image only.
    const btnNext = document.querySelector("#next-image");
    if (btnNext) {
        if (count >= images.length) {
            btnNext.disabled = true;
        } else {
            btnNext.disabled = false;
        }
    }
    // Initial model
    const inputTitle = document.getElementsByName("title")[0];
    if (inputTitle) {
        if (inputTitle.value === "title") {
            inputTitle.value = "";
        } else {
            document.querySelector(".btn.btn-primary").innerHTML = "Save"; // Change the button name 'Create' to 'Edit'
        }
    }

    const inputPrice = document.getElementsByName("price")[0];
    if (inputPrice) {
        if (inputPrice.value === "0.00") {
            inputPrice.value = "";
        }
    }

    const inputDescription = document.getElementsByName("description")[0];
    if (inputDescription) {
        if (inputDescription.value === "description") {
            inputDescription.value = "";
        }
    }

    // Auto Select Category when Edit
    const typeSelect = document.getElementById("type-category");
    const categoryType = document.getElementById("hidden-category-type");
    const categoryTitle = document.getElementById("hidden-category-title");
    if (categoryType) {
        const defaultOption = typeSelect.querySelector(
            `option[value='${categoryType.value}']`
        );
        if (defaultOption) {
            defaultOption.selected = true;
        }
    }
    if (categoryTitle) {
        updateSubCategories();
    }
});

function uploadImage() {
    const fileInput = document.getElementById("image-input");
    const file = fileInput.files[0];
    const product_id = document.getElementById("product-id").value;
    // Fill data inside the form and fetch it
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
            product_id.value = data.product_id; // Hidden input value provide Product ID
            displayImages(data.image_id);

            // Make fileinput become null, To prevent the first image upload again when cancel the second uploading.
            fileInput.value = "";
        })
        .catch((error) => console.error(error));
}

function displayImages(image_id) {
    var previewDiv = document.getElementById("div-order-img");
    var images = document.querySelectorAll("img");
    var btnsDelete = document.querySelectorAll("a");
    var numImages = images.length;
    // Hide all the image and button
    images.forEach((img) => {
        img.style.display = "none";
    });
    btnsDelete.forEach((btn) => {
        btn.style.display = "none";
    });
    // Create image uploaded
    var image = document.createElement("img");
    var btnDelete = document.createElement("a");
    // img url
    image.src = uploadedImages[num];
    num += 1;
    image.className = "img-thumbnail";
    btnDelete.className = "btn btn-danger";

    image.id = `index${numImages.toString()}`;
    btnDelete.id = "index-delete" + numImages.toString();
    btnDelete.innerHTML = "Delete";
    btnDelete.style.position = "absolute";
    btnDelete.onclick = function () {
        const id_num = image.id.split("x")[1];
        deleteImage(image_id, id_num);
    };
    // Show img uploaded
    image.style.display = "block";
    btnDelete.style.display = "block";

    // Set position of count
    count = numImages;
    // Uploaded image at last position, so next should be disabled, and prev be able(prev be disabled if first image).
    document.querySelector("#next-image").disabled = true;
    if (count <= 1) {
        document.querySelector("#prev-image").disabled = true;
    } else {
        document.querySelector("#prev-image").disabled = false;
    }
    // Add uplaoded image to Img View Area
    previewDiv.appendChild(image);
    previewDiv.appendChild(btnDelete);
}

function toggleImage(action) {
    let image;
    const images = document.querySelectorAll(".img-thumbnail");
    const btnsDelete = document.querySelectorAll(".btn.btn-danger");

    // Hide all the img first
    images.forEach((img) => {
        img.style.display = "none";
    });
    // Hide all the delete button first
    btnsDelete.forEach((btn) => {
        btn.style.display = "none";
    });

    // Show/Hide image with toggle buttons 'Prev' and 'Next'/ Delete button
    if (action == "prev") {
        count = count - 1;
        image = document.querySelector(`#index${count}`);
        btn = document.querySelector(`#index-delete${count}`);
        console.log(count);
    } else if (action == "next") {
        count = count + 1;
        image = document.querySelector(`#index${count}`);
        btn = document.querySelector(`#index-delete${count}`);
        console.log(count);
    }
    image.style.display = "block";
    btn.style.display = "block";

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

function deleteImage(image_id, idNum) {
    // Confirm
    const confirmed = confirm("Are you sure you want to delete this image?");

    if (!confirmed) {
        return;
    }

    // Delete image through its ID
    fetch("/delete_image", {
        method: "DELETE",
        body: JSON.stringify({
            image_id: image_id,
        }),
    })
        .then((response) => response.json())
        .then((result) => {
            console.log(result);
            // Length of Images before remove image
            const imagesLength =
                document.querySelectorAll(".img-thumbnail").length;
            // After deleted database's data, remove the display too.
            const imagePrepareToRemove = document.getElementById(
                `index${idNum}`
            );
            const buttonPrepareToRemove = document.getElementById(
                `index-delete${idNum}`
            );

            imagePrepareToRemove.remove();
            buttonPrepareToRemove.remove();

            console.log("idNum:", idNum);
            console.log("imagesLength:" + imagesLength);
            const images = document.querySelectorAll(".img-thumbnail");
            console.log("images.length:" + images.length);
            if (imagesLength > idNum) {
                console.log("images ok");
                images.forEach((img) => {
                    console.log(" each ok");
                    const idImg = img.id.split("x")[1]; // Get the index number. e.g. Get 1 from index1, 2 from index2
                    if (idImg > idNum) {
                        const newID = "index" + (idImg - 1);
                        const btnDelete = document.getElementById(
                            `index-delete${idImg}`
                        );

                        img.id = newID;
                        btnDelete.id = "index-delete" + (idImg - 1);
                        console.log("count" + count);
                    }
                });
            }
            // Show first image if exists.
            if (document.getElementById("index1")) {
                document.getElementById("index1").style.display = "block";
                document.getElementById("index-delete1").style.display =
                    "block";
            }
            // First image, Prev become disabled.
            const btnPrev = document.querySelector("#prev-image");
            btnPrev.disabled = true;
            // Next Image become disabled if there's only 1 image.
            const btnNext = document.querySelector("#next-image");
            count = 1;
            if (count >= images.length) {
                btnNext.disabled = true;
            } else {
                btnNext.disabled = false;
            }
        });
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
            // Add new options based on type categories selected
            result.categories.forEach((category) => {
                const option = document.createElement("option");
                option.text = category.title;
                option.value = category.title;
                subCategorySelect.append(option);
            });
            // Show subCategory select list
            subCategorySelect.style.display = "block";

            // Edit only appear (Auto select title of Category)
            const categoryTitle = document.getElementById(
                "hidden-category-title"
            );
            if (categoryTitle) {
                const defaultOption = subCategorySelect.querySelector(
                    `option[value='${categoryTitle.value}']`
                );
                if (defaultOption) {
                    defaultOption.selected = true;
                } else {
                }
            }
        });
}

function updateProduct() {
    const subCategorySelect = document.getElementById("sub-category");

    fetch("/create_order/category_select", {
        method: "PUT",
        body: JSON.stringify({
            category_select: subCategorySelect.value,
        }),
    })
        .then((response) => response.json())
        .then((result) => {
            console.log(result);
            const productSelect = document.getElementById("product-select");
            // Remove existing product options
            productSelect.innerHTML = "<option selected>Product</option>";
            // add new options based on sub categories selected
            result.product.forEach((product) => {
                const option = document.createElement("option");
                option.text = product.title;
                option.value = product.title;
                productSelect.append(option);
            });
            // Show product select list
            productSelect.style.display = "block";
            // Select product, then
            productSelect.onchange = () => {
                document.getElementById("create-next").style.display = "block";
                const btnCreateNext =
                    document.getElementById("btn-create-next");
                btnCreateNext.onclick = () => {
                    const url = `/create_order/details/${productSelect.value}`;
                    window.location.href = url;
                };
            };
        })
        .catch((error) => console.error(error));
}
