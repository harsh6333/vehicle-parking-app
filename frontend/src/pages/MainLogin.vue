<template>
  <div class="container mt-5">
    <h2 class="text-center">Login</h2>
    <div class="form-group mt-4">
      <input
        v-model="email"
        class="form-control"
        placeholder="Email"
        type="email"
      />
      <input
        v-model="password"
        class="form-control mt-2"
        placeholder="Password"
        type="password"
      />
      <button @click="handleLogin" class="btn btn-primary mt-3 w-100">
        Login
      </button>
      <p v-if="error" class="text-danger mt-2">{{ error }}</p>
    </div>

    <div class="text-center mt-3">
      <router-link to="/register" class="btn btn-outline-secondary btn-sm">
        Don’t have an account? Register
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/auth";

const email = ref("");
const password = ref("");
const error = ref("");
const router = useRouter();
const auth = useAuthStore();

const handleLogin = async () => {
  error.value = "";
  try {
    const res = await axios.post("http://127.0.0.1:5000/api/auth/login", {
      email: email.value,
      password: password.value,
    });

    auth.login(res.data);

    if (auth.isAdmin) {
      router.push("/admin/dashboard");
    } else {
      router.push("/user/dashboard");
    }
  } catch (err) {
    error.value = err.response?.data?.msg || "Login failed";
  }
};
</script>
