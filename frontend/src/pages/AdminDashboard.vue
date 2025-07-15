<template>
  <div class="container mt-5">
    <h2>Admin Dashboard</h2>
    <div class="alert alert-success mt-3">Welcome, {{ auth.username }}! 👑</div>
  </div>
</template>

<script setup>
import { useAuthStore } from "@/store/auth";
const auth = useAuthStore();
</script>
