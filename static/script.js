document.addEventListener("DOMContentLoaded", function() {
    const amountError = document.getElementById("amountError"),
        propError = document.getElementById("propError"),
        dateError = document.getElementById("dateError"),
        datePicker = document.getElementById("datePicker"),
        monthPicker = document.getElementById("monthPicker"),
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

    function isEmpty(field) {
        if(!field.value) {
            return true;
        }

        return false;
    }

    function validateProp(field) {
        if(sharedBox.checked) {
            if(isEmpty(prop1) || isEmpty(prop2)) {
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
        if(isEmpty(amount1) && isEmpty(amount2)) {
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

    function validateDate(field) {
        if(isEmpty(field)) {
            showError(dateError, "Date field should not be empty")
            return false;
        }

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

        [prop1, prop2].forEach(validateProp);
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

    datePicker.addEventListener("change", function() {
        validateDate(datePicker);
    });

    form.addEventListener("submit", function(event) {
        if(!(validateAmount(amount1) &&
        validateAmount(amount2) &&
        validateProp(prop1) &&
        validateProp(prop2) &&
        validateDate(datePicker))) {
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

    monthPicker.addEventListener("change", function() {
        if(!isEmpty(this)) {
            window.location.href = `/month/${this.value}`;
        }
    });
});

window.onload = function() {
    let today = new Date().toISOString().split('T')[0];
    let chosenDate = window.location.search.slice(-10);
    
    document.getElementById("datePicker").value = today;
    if(chosenDate) {
        document.getElementById("monthPicker").value = window.location.search.slice(-10);
    }
    else {
        document.getElementById("monthPicker").value = today;
    }
};