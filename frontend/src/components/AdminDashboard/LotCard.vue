<template>
  <div class="card lot-card h-100 border-0 shadow-sm mb-3">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-start mb-2">
        <h5 class="card-title mb-0 text-primary">
          <i class="bi bi-geo-alt-fill me-2"></i>
          {{ lot.prime_location_name }}
        </h5>
        <span class="badge bg-primary bg-opacity-10 text-primary">
          {{ lot.total_spots }} spots
        </span>
      </div>

      <div class="mb-2 text-muted small">
        <div><i class="bi bi-geo"></i> {{ lot.address }}</div>
        <div><i class="bi bi-postcard"></i> PIN: {{ lot.pin_code }}</div>
        <div><i class="bi bi-cash-coin"></i> ₹{{ lot.price }} / hr</div>
      </div>

      <button
        class="btn btn-sm btn-outline-primary w-100"
        @click="$emit('viewSpots', lot.id)"
      >
        <i class="bi bi-eye me-1"></i> View Spots
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps(["lot"]);
defineEmits(["viewSpots"]);
</script>

<style scoped>
.lot-card {
  border-radius: 12px;
}
</style>
