const editProfile = document.getElementById("btnEdit");
const editPassword = document.getElementById("btnPassword");

editProfile.addEventListener("click", function (e) {
  const form = document.getElementById("editForm");
  form.classList.toggle("d-none");
  if (e.target.innerHTML !== "Edit Profil") {
    return (e.target.innerHTML = "Edit Profil");
  }
  return (e.target.innerHTML = "Batal");
});

editPassword.addEventListener("click", function (e) {
  const password = document.getElementById("passwordForm");
  const passwordInput = document.getElementById("passwordInput");
  if (!!passwordInput) {
    passwordInput.remove();
  }
  const passwordInputEl = `<input id="passwordInput" class="form-control" type="password" name="password" >`;
  const passwordContainer = document.getElementById("passwordContainer");
  passwordContainer.insertAdjacentHTML("afterbegin", passwordInputEl);

  password.classList.toggle("d-none");
  if (e.target.innerHTML !== "Ubah Password") {
    return (e.target.innerHTML = "Ubah Password");
  }
  return (e.target.innerHTML = "Batal");
});
