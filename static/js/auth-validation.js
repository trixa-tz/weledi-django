// Client-side validation for the auth & publish forms.
// Behaviour: validate ONLY when the user clicks submit. If errors are shown,
// the next interaction with the form (typing/changing any field) clears ALL
// errors and waits for the user to submit again. No live/on-type validation.
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
        markInvalid(input);
        var msg = document.createElement("p");
        msg.className = "field-error mt-1.5 text-xs text-red-600";
        msg.textContent = message;
        fieldContainer(input).appendChild(msg);
    }

    function markInvalid(input) {
        input.classList.add("border-red-400", "focus:ring-red-100");
        input.classList.remove("border-slate-300", "focus:ring-brand-100");
    }

    function resetField(input) {
        input.classList.remove("border-red-400", "focus:ring-red-100");
        input.classList.add("border-slate-300", "focus:ring-brand-100");
    }

    // Wipe every error in the form and restore all field styles.
    function clearAllErrors(form) {
        form.querySelectorAll(".field-error").forEach(function (el) { el.remove(); });
        form.querySelectorAll("input, textarea").forEach(resetField);
    }

    // Validate a single field; show an error and return false if invalid.
    function checkField(input) {
        var value = (input.value || "").trim();

        if (input.hasAttribute("required") && value === "") {
            showError(input, "This field is required.");
            return false;
        }
        if (input.name === "username" && value.length < 3) {
            showError(input, "Username must be at least 3 characters.");
            return false;
        }
        if (input.name === "password" && value.length < 8) {
            showError(input, "Password must be at least 8 characters.");
            return false;
        }
        if (input.name === "phone" && value !== "" && !/^[+0-9()\s-]{7,}$/.test(value)) {
            showError(input, "Please enter a valid phone number.");
            return false;
        }
        return true;
    }

    function init() {
        var forms = document.querySelectorAll("form[data-validate]");

        forms.forEach(function (form) {
            var fields = form.querySelectorAll("input, textarea");
            var showingErrors = false;

            form.addEventListener("submit", function (e) {
                var ok = true;
                fields.forEach(function (input) {
                    if (!checkField(input)) ok = false;
                });

                // Confirm-password match (signup form only).
                var pwd = form.querySelector('input[name="password"]');
                var pwd2 = form.querySelector('input[name="password2"]');
                if (pwd && pwd2 && pwd.value !== pwd2.value) {
                    showError(pwd2, "Passwords do not match.");
                    ok = false;
                }

                if (!ok) {
                    e.preventDefault();
                    showingErrors = true;
                }
            });

            // Any interaction after errors are shown clears them and waits
            // for the next submit. No re-validation happens while typing.
            function resetOnInteract() {
                if (showingErrors) {
                    clearAllErrors(form);
                    showingErrors = false;
                }
            }
            form.addEventListener("input", resetOnInteract);
            form.addEventListener("change", resetOnInteract);
        });

        // Password visibility toggles (eye / eye-off).
        document.querySelectorAll("[data-toggle-password]").forEach(function (btn) {
            btn.addEventListener("click", function () {
                var input = document.getElementById(btn.getAttribute("data-toggle-password"));
                if (!input) return;
                var reveal = input.type === "password";
                input.type = reveal ? "text" : "password";
                var eye = btn.querySelector("[data-eye]");
                var eyeOff = btn.querySelector("[data-eye-off]");
                if (eye) eye.classList.toggle("hidden", reveal);
                if (eyeOff) eyeOff.classList.toggle("hidden", !reveal);
                btn.setAttribute("aria-label", reveal ? "Hide password" : "Show password");
            });
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
