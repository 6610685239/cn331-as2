// Function to toggle password visibility
function togglePassword(inputId) {
    var passwordField = document.getElementById(inputId);
    var icon = passwordField.nextElementSibling;
    if (passwordField.type === "password") {
        passwordField.type = "text";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    } else {
        passwordField.type = "password";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    }
}

// Example login JS validation (optional)
const loginForm = document.querySelector("form");
const usernameField = loginForm.querySelector(".field:nth-of-type(1)"),
      usernameInput = usernameField.querySelector("input"),
      passwordField = loginForm.querySelector(".field:nth-of-type(2)"),
      passwordInput = passwordField.querySelector("input");

loginForm.onsubmit = (e) => {
    e.preventDefault();

    // Clear previous errors
    usernameField.classList.remove("error");
    passwordField.classList.remove("error");
    let hasError = false;

    // Check if fields are empty
    if (usernameInput.value.trim() === "") {
        usernameField.classList.add("error");
        hasError = true;
    }

    if (passwordInput.value.trim() === "") {
        passwordField.classList.add("error");
        hasError = true;
    }

    if (!hasError) {
        loginForm.submit();
    }
};

// Remove error class on input keyup
usernameInput.onkeyup = () => {
    if (usernameInput.value.trim() !== "") {
        usernameField.classList.remove("error");
    }
};

passwordInput.onkeyup = () => {
    if (passwordInput.value.trim() !== "") {
        passwordField.classList.remove("error");
    }
};
