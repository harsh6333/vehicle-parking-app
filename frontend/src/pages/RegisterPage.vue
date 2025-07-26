<template>
  <div class="container-fluid min-vh-100 d-flex p-0">
    <!-- Left: Registration Form -->
    <div
      class="col-lg-5 d-flex align-items-center justify-content-center bg-white"
    >
      <div class="p-4 p-md-5 w-100" style="max-width: 400px">
        <div class="mb-4 text-center">
          <h2 class="fw-bold text-success">Register</h2>
          <p class="text-muted">Create your parking account</p>
        </div>

        <!-- Username -->
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <div class="input-group">
            <span class="input-group-text bg-light">
              <i class="bi bi-person-fill"></i>
            </span>
            <input
              v-model="username"
              type="text"
              id="username"
              class="form-control"
              placeholder="Enter username"
            />
          </div>
        </div>

        <!-- Email -->
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <div class="input-group">
            <span class="input-group-text bg-light">
              <i class="bi bi-envelope-fill"></i>
            </span>
            <input
              v-model="email"
              type="email"
              id="email"
              class="form-control"
              placeholder="Enter email"
            />
          </div>
        </div>

        <!-- Password -->
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <div class="input-group">
            <span class="input-group-text bg-light">
              <i class="bi bi-lock-fill"></i>
            </span>
            <input
              v-model="password"
              type="password"
              id="password"
              class="form-control"
              placeholder="Enter password"
            />
          </div>
        </div>

        <!-- Register Button -->
        <button @click="handleRegister" class="btn btn-success w-100 mb-3">
          Register
        </button>

        <!-- Alerts -->
        <div v-if="error" class="alert alert-danger text-center py-2">
          {{ error }}
        </div>
        <div v-if="success" class="alert alert-success text-center py-2">
          {{ success }}
        </div>

        <!-- Login Link -->
        <div class="text-center mt-3">
          <small>
            Already have an account?
            <router-link to="/login" class="fw-semibold text-decoration-none">
              Login here
            </router-link>
          </small>
        </div>
      </div>
    </div>

    <!-- Right: Illustration -->
    <div
      class="col-lg-7 d-none d-lg-flex align-items-center justify-content-center bg-light"
    >
      <img
        src="@/assets/heroImage.png"
        alt="Register Illustration"
        class="img-fluid p-5"
        style="max-height: 80%"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const username = ref("");
const email = ref("");
const password = ref("");
const error = ref("");
const success = ref("");
const router = useRouter();

const handleRegister = async () => {
  error.value = "";
  success.value = "";
  try {
    await axios.post("http://127.0.0.1:5000/api/auth/register", {
      username: username.value,
      email: email.value,
      password: password.value,
    });
    success.value = "Registration successful! Redirecting...";
    setTimeout(() => router.push("/login"), 1500);
  } catch (err) {
    error.value = err.response?.data?.msg || "Registration failed";
  }
};
</script>

<style scoped>
body {
  background-color: #f7fafd;
}
</style>
