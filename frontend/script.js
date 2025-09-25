// Predefined credentials (simulation)
// Replace with backend auth in production
const users = {
  stakeholder: { username: "stake", password: "stake123", page: "stake2.html" },
  manager: { username: "manager", password: "manager123", page: "dashManager.html" },
  user: { username: "user", password: "user123", page: "user.html" }
};

document.getElementById("loginForm").addEventListener("submit", function(e) {
  e.preventDefault();

  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();
  const role = document.getElementById("role").value;

  if (role && users[role]) {
    const validUser = users[role];
    if (username === validUser.username && password === validUser.password) {
      localStorage.setItem("loggedInRole", role);
      window.location.href = validUser.page;
      return;
    }
  }

  document.getElementById("errorMsg").classList.remove("hidden");
});

