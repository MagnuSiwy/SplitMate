document.addEventListener("DOMContentLoaded", function() {
    const amountError = document.getElementById("amountError"),
        propError = document.getElementById("propError"),
        month = document.getElementById("monthPicker"),
        category = document.getElementById("categorySelect"),
        prop1 = document.getElementById("prop1"),
        prop2 = document.getElementById("prop2"),
        amount1 = document.getElementById("amount1"),
        amount2 = document.getElementById("amount2"),
        sharedBox = document.getElementById("isShared"),
        form = document.getElementById("budgetForm");

    function showError(field, message) {
        field.innerText = message;
        field.style.display = "block";
    }

    function clearError(field) {
        field.style.display = "none";
    }

    function validateProp(field) {
        if(sharedBox.checked) {
            if(!(prop1.value && prop2.value)) {
                showError(propError, "At least one of the PROPORTION fields should be used with a numerical values");
                return false;
            }

            if(field.value < 0) {
                showError(propError, "PROPORTIONS value should be greater than 0");
                return false;
            }
        }

        clearError(propError);
        return true;
    }

    function validateAmount(field) {
        if(!(amount1.value || amount2.value)) {
            showError(amountError, "At least one of the AMOUNT fields should be used with a numerical value");
            return false;
        }

        if(field.value < 0 && sharedBox.checked) {
            showError(amountError, "Amount to split should be greater than 0")
            return false;
        }
        
        clearError(amountError);
        return true;
    }

    document.getElementById("categorySelect").addEventListener("change", function() {
        if(category.value == "Food") {
            prop1.value = 3;
            prop2.value = 5;
            sharedBox.checked = true;
        }
        else if(category.value == "Clothes" ||
        category.value == "Cosmetics") {
            prop1.value = "";
            prop2.value = "";
            sharedBox.checked = false;
        }
        else {
            sharedBox.checked = true;
            prop1.value = 1;
            prop2.value = 1;
        }
    });

    [amount1, amount2].forEach(field => {
        field.addEventListener("input", function() {
            validateAmount(field);
        });
    });

    [prop1, prop2].forEach(field => {
        field.addEventListener("input", function() {
            validateProp(field);
        });
    });

    sharedBox.addEventListener("change", function() {
        if(!sharedBox.checked) {
            clearError(propError);
        }
        else {
            [prop1, prop2].forEach(validateProp);
        }
    });

    form.addEventListener("submit", function(event) {
        if(!(validateAmount(amount1) &&
        validateAmount(amount2) &&
        validateProp(prop1) &&
        validateProp(prop2))) {
            event.preventDefault();
        }
    });

    document.querySelectorAll("#idButton").forEach(button => {
        button.addEventListener("click", function() {
            let recordID = this.getAttribute("record-id");

            fetch(`/delete/${recordID}`, {
                method: "POST"
            })
            .then(() => {
                location.reload();
            })
            .catch((error) => {
                console.error("Error:", error);
            });
        });
    });

    document.getElementById("monthPicker").addEventListener("change", function() {
        window.location.href = `/month/${this.value}`;
    });
});

window.onload = function() {
    let today = new Date().toISOString().split('T')[0];
    document.getElementById("datePicker").value = today;
};