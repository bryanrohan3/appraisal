<template>
  <div class="navbar-wrapper">
    <div class="navbar">
      <div class="logo-container">
        <img src="@/assets/logo.svg" class="logo" />
        <p class="company">i@ppraisal</p>
      </div>
      <router-link to="dashboard">
        <div class="nav-item">
          <img src="@/assets/dashboard.svg" class="icon" />
          <a href="/">Dashboard</a>
        </div>
      </router-link>

      <router-link to="/#">
        <a class="nav-item">
          <img src="@/assets/search.svg" class="icon" />
          <a>Search</a>
        </a>
      </router-link>

      <router-link to="/#">
        <div class="nav-item">
          <img src="@/assets/appraisal-icon.svg" class="icon" />
          <a>Appraisals</a>
        </div>
      </router-link>

      <router-link to="create-appraisal">
        <div class="nav-item">
          <img src="@/assets/create-appraisal.svg" class="icon" />
          <a>Create</a>
        </div>
      </router-link>

      <router-link to="/#">
        <div class="nav-item">
          <img src="@/assets/analytics.svg" class="icon" />
          Analytics
        </div>
      </router-link>

      <router-link to="/#">
        <div class="nav-item">
          <img src="@/assets/requests.svg" class="icon" />
          Requests
        </div>
      </router-link>

      <!-- Add logout button here -->
      <div class="logout-container">
        <button @click="handleLogout" class="logout-button">
          <img src="@/assets/logout.svg" class="logout-icon" />
          Logout
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapMutations } from "vuex";

export default {
  name: "DealerNavBar",
  methods: {
    ...mapMutations(["logout"]),
    handleLogout() {
      this.logout(); // Clear Vuex state
      this.$router.push({ name: "login" }); // Redirect to login page
    },
  },
};
</script>

<style scoped>
@font-face {
  font-family: "LogoFont"; /* Choose a name for your font */
  src: url("@/assets/fonts/AirbnbCereal_W_Blk.otf") format("opentype");
  font-weight: normal;
  font-style: normal;
}

html,
body {
  height: 100%;
  margin: 0;
  padding: 0;
  background-color: #ffffff;
}

.icon {
  margin-right: 10px;
}

.logo-container {
  display: flex;
  align-items: center;
  padding-left: 10px;
  margin-top: 20px;
}

.logo {
  width: 30px; /* Adjust size as needed */
  height: auto;
  margin-right: 10px;
}

.company {
  font-weight: 800;
  font-size: 24px;
  color: #f26764;
  font-weight: 600;
  font-family: "LogoFont";
}

.navbar-wrapper {
  height: 100vh; /* Full viewport height */
  position: fixed; /* Fix the navbar */
  display: flex;
}

.navbar {
  width: 200px; /* Adjust width as needed */
  height: 100vh; /* Full viewport height */
  background-color: #ffffff; /* Example background color */
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* Space between nav items and logout button */
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
}

.nav-item {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  color: #333;
}

.nav-item:hover {
  background-color: #f1f1f1;
}

.nav-item svg {
  margin-right: 10px;
}

.navbar a {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  font-size: 16px;
}

.nav-item .icon {
  transition: transform 0.3s ease;
}

.nav-item:hover .icon {
  transform: scale(1.1);
}

.logout-container {
  margin-top: auto; /* Pushes the logout button to the bottom */
  padding: 10px;
}

.logout-button {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 10px;
  margin-top: auto; /* Ensure it stays at the bottom */
  border-radius: 5px;
  color: #f26764;
  background: #ffffff;
  border: 3px solid #ffffff;
  border-radius: 10px;
  margin-bottom: 50px;
  width: 100%;
  font-weight: 800;
  font-size: 16px;
}

.logout-button:hover {
  background-color: #f1f1f1;
}

.logout-icon {
  margin-right: 10px;
}
</style>
