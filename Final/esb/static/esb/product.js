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

let count = 1;
let image;

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
