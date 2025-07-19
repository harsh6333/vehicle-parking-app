<template>
  <div class="d-flex justify-content-between align-items-center mb-4">
    <div>
      <h2 class="fw-bold mb-1">Welcome back, {{ username }}</h2>
      <p class="text-muted mb-0">Manage your parking reservations</p>
    </div>
    <button class="btn btn-success" @click="$emit('quickReserve')">
      <i class="bi bi-magic me-1"></i> Quick Reserve
    </button>
  </div>
</template>

<script setup>
defineProps({
  username: String,
});

defineEmits(["quickReserve"]);
</script>
