let changePasswordForm = document.getElementById('change-password-form');
let changePasswordButton = document.getElementById('change-password-button');
let newPassword = document.getElementById('new-password');
let confirmNewPassword = document.getElementById('confirm-new-password');
let oldPassword = document.getElementById('old-password');
let passwordError = document.getElementById('error');

changePasswordButton.addEventListener('click', async function (e) {
    e.preventDefault();
    changePasswordButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
    let formData = new FormData(changePasswordForm);
    formData = {
        old_password: formData.get('old_password'),
        new_password: formData.get('new_password'),
        confirm_new_password: formData.get('confirm_new_password'),
    }
    let url = "/api/v1/change-password/";
    const response = await sendPostRequest(url, formData)
        .then((data) => {
            console.log(data);
            if (data.status === 'success') {
                changePasswordForm.reset();
                changePasswordButton.innerHTML = 'Success';
                setTimeout(() => {
                    changePasswordButton.innerHTML = 'Change Password';
                }, 3000);
            } else {
                if (data.old_password) {
                    oldPassword.innerHTML = data.old_password;
                } else if (data.new_password) {
                    newPassword.innerHTML = data.new_password;
                } else if (data.confirm_new_password) {
                    confirmNewPassword.innerHTML = data.confirm_new_password;
                } else if (data.error) {
                    passwordError.innerHTML = data.error;
                }
                changePasswordButton.innerHTML = 'Failed! Try Again';
                setTimeout(() => {
                    changePasswordButton.innerHTML = 'Change Password';
                }, 3000);
            }
        })
        .catch((error) => {
            console.log(error);
        });

});
