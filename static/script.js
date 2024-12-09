document.addEventListener("DOMContentLoaded", () => {
    const deleteButtons = document.querySelectorAll("form[action$='/delete'] button");

    deleteButtons.forEach((button) => {
        button.addEventListener("click", (event) => {
            const confirmation = confirm("Are you sure you want to delete this item?");
            if (!confirmation) {
                event.preventDefault();
            }
        });
    });
});

const forms = document.querySelectorAll("form");

forms.forEach((form) => {
    form.addEventListener("submit", (event) => {
        const requiredFields = form.querySelectorAll("[required]");
        let allValid = true;

        requiredFields.forEach((field) => {
            if (!field.value.trim()) {
                allValid = false;
                field.style.border = "2px solid red";
            } else {
                field.style.border = "";
            }
        });

        if (!allValid) {
            event.preventDefault();
            alert("Please fill out all required fields.");
        }
    });
});
