<template>
  <div class="container mt-5">
    <h2>User Dashboard</h2>
    <div class="alert alert-info mt-3">Welcome, {{ auth.username }}!</div>
  </div>
</template>

<script setup>
import { useAuthStore } from "@/store/auth";
const auth = useAuthStore();
</script>
