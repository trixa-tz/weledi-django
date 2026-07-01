// Client-side validation for the login & signup forms.
// Runs before the form is submitted and shows inline error messages.
// The server still validates everything again. This is just for UX.

(function () {
    "use strict";

    // Where the error text lives: OUTSIDE the icon wrapper (.relative) so it
    // never grows that box and pushes the vertically-centered icon out of place.
    function fieldContainer(input) {
        var wrapper = input.closest(".relative");
        return wrapper ? wrapper.parentNode : input.parentNode;
    }

    function showError(input, message) {
        clearError(input);
        input.classList.add("border-red-400", "focus:ring-red-100");
        input.classList.remove("border-slate-300", "focus:ring-brand-100");

        var msg = document.createElement("p");
        msg.className = "field-error mt-1.5 text-xs text-red-600";
        msg.textContent = message;
        fieldContainer(input).appendChild(msg);
    }

    function clearError(input) {
        input.classList.remove("border-red-400", "focus:ring-red-100");
        input.classList.add("border-slate-300", "focus:ring-brand-100");
        var existing = fieldContainer(input).querySelector(".field-error");
        if (existing) existing.remove();
    }

    function validateField(input) {
        var value = (input.value || "").trim();

        if (input.hasAttribute("required") && value === "") {
            showError(input, "This field is required.");
            return false;
        }

        if (input.name === "username" && value !== "" && value.length < 3) {
            showError(input, "Username must be at least 3 characters.");
            return false;
        }

        if (input.name === "password" && value !== "" && value.length < 8) {
            showError(input, "Password must be at least 8 characters.");
            return false;
        }

        if (input.name === "phone" && value !== "" && !/^[+0-9()\s-]{7,}$/.test(value)) {
            showError(input, "Please enter a valid phone number.");
            return false;
        }

        clearError(input);
        return true;
    }

    function init() {
        var forms = document.querySelectorAll("form[data-validate]");

        forms.forEach(function (form) {
            var inputs = form.querySelectorAll("input");

            // Live validation as the user leaves / edits a field.
            inputs.forEach(function (input) {
                input.addEventListener("blur", function () { validateField(input); });
                input.addEventListener("input", function () {
                    if (fieldContainer(input).querySelector(".field-error")) validateField(input);
                });
            });

            form.addEventListener("submit", function (e) {
                var ok = true;

                inputs.forEach(function (input) {
                    if (!validateField(input)) ok = false;
                });

                // Confirm-password match (signup form only).
                var pwd = form.querySelector('input[name="password"]');
                var pwd2 = form.querySelector('input[name="password2"]');
                if (pwd && pwd2 && pwd2.value !== "" && pwd.value !== pwd2.value) {
                    showError(pwd2, "Passwords do not match.");
                    ok = false;
                }

                if (!ok) e.preventDefault();
            });
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
