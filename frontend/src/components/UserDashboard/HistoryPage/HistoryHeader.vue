<template>
  <div class="d-flex justify-content-between align-items-center mb-4 flex-wrap">
    <div class="mb-2 mb-md-0">
      <h2 class="fw-bold mb-1">
        <i class="bi bi-clock-history text-primary me-2"></i>
        Reservation History
      </h2>
      <p class="text-muted mb-0">
        View your past and current parking reservations
      </p>
    </div>
    <!-- <div class="d-flex gap-2 flex-wrap">
      <div class="input-group" style="width: 200px">
        <span class="input-group-text">
          <i class="bi bi-calendar"></i>
        </span>
        <input
          type="date"
          :v-model="modelValue"
          class="form-control"
          @change="$emit('update')"
        />
      </div>
    </div> -->
  </div>
</template>

<script setup>
defineProps(["modelValue"]);
defineEmits(["update"]);
</script>
