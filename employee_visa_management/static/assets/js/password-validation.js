document.getElementById("password1").addEventListener("input", function() {
    var password = this.value;

    // Check if password is 8 characters long
    document.getElementById("8char").classList.toggle("glyphicon-ok", password.length >= 8);
    document.getElementById("8char").classList.toggle("glyphicon-remove", password.length < 8);
    document.getElementById("check8char").checked = password.length >= 8;

    // Check if password has at least one uppercase letter
    document.getElementById("ucase").classList.toggle("glyphicon-ok", /[A-Z]/.test(password));
    document.getElementById("ucase").classList.toggle("glyphicon-remove", !/[A-Z]/.test(password));
    document.getElementById("checkUcase").checked = /[A-Z]/.test(password);

    // Check if password has at least one lowercase letter
    document.getElementById("lcase").classList.toggle("glyphicon-ok", /[a-z]/.test(password));
    document.getElementById("lcase").classList.toggle("glyphicon-remove", !/[a-z]/.test(password));
    document.getElementById("checkLcase").checked = /[a-z]/.test(password);

    // Check if password has at least one number
    document.getElementById("num").classList.toggle("glyphicon-ok", /[0-9]/.test(password));
    document.getElementById("num").classList.toggle("glyphicon-remove", !/[0-9]/.test(password));
    document.getElementById("checkNum").checked = /[0-9]/.test(password);
});

document.getElementById("password2").addEventListener("input", function() {
    var password1 = document.getElementById("password1").value;
    var password2 = this.value;

    // Check if passwords match
    document.getElementById("pwmatch").classList.toggle("glyphicon-ok", password1 === password2 && password1 !== "" && password2 !== "");
    document.getElementById("pwmatch").classList.toggle("glyphicon-remove", password1 !== password2 || password1 === "" || password2 === "");
    document.getElementById("checkPwmatch").checked = password1 === password2 && password1 !== "" && password2 !== "";
});

document.getElementById("validationAgree").addEventListener("change", function() {
    var checkbox = this;
    var submitBtn = document.querySelector("#passwordForm input[type='submit']");

    if (checkbox.checked) {
        submitBtn.removeAttribute("disabled");
    } else {
        submitBtn.setAttribute("disabled", "disabled");
    }
});