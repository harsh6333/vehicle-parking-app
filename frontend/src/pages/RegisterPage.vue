<template>
  <div class="container mt-5">
    <h2 class="text-center">Create an Account</h2>
    <div class="form-group mt-4">
      <input
        v-model="username"
        class="form-control"
        placeholder="Username"
        type="text"
      />
      <input
        v-model="email"
        class="form-control mt-2"
        placeholder="Email"
        type="email"
      />
      <input
        v-model="password"
        class="form-control mt-2"
        placeholder="Password"
        type="password"
      />
      <button @click="handleRegister" class="btn btn-success mt-3 w-100">
        Register
      </button>
      <p v-if="error" class="text-danger mt-2">{{ error }}</p>
      <p v-if="success" class="text-success mt-2">{{ success }}</p>
    </div>

    <div class="text-center mt-3">
      <router-link to="/login" class="btn btn-outline-secondary btn-sm">
        Back to Login
      </router-link>
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
    success.value = "Registration successful! Redirecting to login...";
    setTimeout(() => router.push("/login"), 1500);
  } catch (err) {
    error.value = err.response?.data?.msg || "Registration failed";
  }
};
</script>
