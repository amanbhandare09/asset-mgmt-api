// Attach token automatically
function getToken() {
    return localStorage.getItem("token");
}

// Claim asset
async function claimAsset(id) {

    const res = await fetch(`/cashback/${id}/claim`, {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + getToken()
        }
    });

    const data = await res.json();

    alert(JSON.stringify(data));
    location.reload();
}


// Login handler
const loginForm = document.getElementById("loginForm");

if (loginForm) {

loginForm.onsubmit = async e => {

e.preventDefault();

const res = await fetch("/auth/login", {
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
email:email.value,
password:password.value
})
});

const data = await res.json();

localStorage.setItem("token", data.access_token);
localStorage.setItem("role", data.role);

// Redirect based on role
if (data.role === "ADMIN") {
window.location.href = "/admin/";
} else {
window.location.href = "/cashback/dashboard";
}

};
}



// Register handler
const regForm = document.getElementById("registerForm");

if (regForm) {

    regForm.onsubmit = async e => {

        e.preventDefault();

        await fetch("/auth/register", {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify({
                email: email.value,
                password: password.value
            })
        });

        alert("Registered successfully");
        window.location.href="/auth/login-page";

    };
}


// Create asset
const assetForm = document.getElementById("assetForm");

if (assetForm) {

    assetForm.onsubmit = async e => {

        e.preventDefault();

        await fetch("/admin/assets/create", {
            method: "POST",
            headers: {
                "Content-Type":"application/json",
                "Authorization":"Bearer " + getToken()
            },
            body: JSON.stringify({
                title: title.value,
                value: value.value
            })
        });

        alert("Asset created");
    };
}

function logout(){

    fetch("/auth/logout");

    localStorage.clear();

    window.location.href="/";
}

