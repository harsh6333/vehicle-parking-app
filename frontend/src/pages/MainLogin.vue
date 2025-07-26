<template>
  <div class="container-fluid min-vh-100 d-flex p-0">
    <!-- Left: Login Card -->
    <div
      class="col-lg-5 d-flex align-items-center justify-content-center bg-white"
    >
      <div class="p-4 p-md-5 w-100" style="max-width: 400px">
        <div class="mb-4 text-center">
          <h2 class="fw-bold">Login</h2>
          <p class="text-muted">Access your parking dashboard</p>
        </div>

        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <div class="input-group">
            <span class="input-group-text bg-light"
              ><i class="bi bi-envelope-fill"></i
            ></span>
            <input
              v-model="email"
              type="email"
              id="email"
              class="form-control"
              placeholder="you@example.com"
            />
          </div>
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <div class="input-group">
            <span class="input-group-text bg-light"
              ><i class="bi bi-lock-fill"></i
            ></span>
            <input
              v-model="password"
              type="password"
              id="password"
              class="form-control"
              placeholder="Enter your password"
            />
          </div>
        </div>

        <div class="d-flex justify-content-between align-items-center mb-3">
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="remember" />
            <label class="form-check-label" for="remember">Remember me</label>
          </div>
          <a href="#" class="small text-decoration-none text-primary"
            >Forgot password?</a
          >
        </div>

        <button @click="handleLogin" class="btn btn-primary w-100 mb-3">
          Login
        </button>

        <div v-if="error" class="alert alert-danger text-center py-2">
          {{ error }}
        </div>

        <div class="text-center mb-3">
          <small
            >Don't have an account?
            <router-link to="/register" class="fw-semibold text-decoration-none"
              >Register</router-link
            >
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
        alt="Login Illustration"
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

const email = ref("");
const password = ref("");
const error = ref("");
const router = useRouter();

const handleLogin = async () => {
  error.value = "";
  try {
    await axios.post(
      "http://127.0.0.1:5000/api/auth/login",
      {
        email: email.value,
        password: password.value,
      },
      {
        withCredentials: true,
      }
    );

    const res = await axios.get("http://127.0.0.1:5000/api/auth/me", {
      withCredentials: true,
    });

    const user = res.data;
    router.push(user.is_admin ? "/admin/dashboard" : "/user/dashboard");
  } catch (err) {
    error.value = err.response?.data?.msg || "Login failed";
  }
};
</script>

<style scoped>
body {
  background-color: #f7fafd;
}
</style>
