<template>
  <div class="card h-100 border-0 shadow-sm lot-card">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-start mb-3">
        <div>
          <h5 class="fw-bold mb-1">{{ lot.prime_location_name }}</h5>
          <p class="text-muted small mb-2">
            <i class="bi bi-geo-alt me-1"></i>
            {{ lot.address }}
          </p>
        </div>
        <span class="badge bg-success-subtle text-success">
          ₹{{ lot.price }}/hr
        </span>
      </div>

      <SpotGrid
        :spots="lot.spots"
        @reserve="(spotId) => $emit('reserve', spotId)"
      />

      <button
        class="btn btn-outline-primary w-100 mt-3"
        @click="$emit('viewDetails', lot.id)"
      >
        View All Spots
      </button>
    </div>
  </div>
</template>

<script setup>
import SpotGrid from "./SpotGrid.vue";

defineProps({
  lot: Object,
});

defineEmits(["reserve", "viewDetails"]);
</script>

<style scoped>
.lot-card {
  border-radius: 0.75rem;
  transition: transform 0.2s;
  border-left: 4px solid #0d6efd;
}

.lot-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1) !important;
}
</style>
