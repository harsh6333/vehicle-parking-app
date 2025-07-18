<template>
  <div class="card lot-card h-100 border-0 shadow-sm">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-start mb-2">
        <h5 class="card-title mb-0 text-primary">
          <i class="bi bi-geo-alt-fill me-2"></i>
          {{ lot.prime_location_name }}
        </h5>
        <span class="badge bg-primary bg-opacity-10 text-primary">
          {{ lot.number_of_spots }} spots
        </span>
      </div>

      <div class="lot-details mb-3">
        <div class="d-flex align-items-center mb-1">
          <i class="bi bi-geo me-2 text-muted"></i>
          <small class="text-muted">{{ lot.address }}</small>
        </div>
        <div class="d-flex align-items-center mb-1">
          <i class="bi bi-postcard me-2 text-muted"></i>
          <small class="text-muted">PIN: {{ lot.pin_code }}</small>
        </div>
        <div class="d-flex align-items-center">
          <i class="bi bi-cash-coin me-2 text-muted"></i>
          <small class="text-muted">₹{{ lot.price }} / hour</small>
        </div>
      </div>

      <div class="d-flex gap-2">
        <button
          @click="$emit('viewSpots', lot.id)"
          class="btn btn-sm btn-outline-primary flex-grow-1"
        >
          <i class="bi bi-car-front me-1"></i> Spots
        </button>
        <button
          @click="$emit('editLot', lot)"
          class="btn btn-sm btn-outline-secondary"
          title="Edit"
        >
          <i class="bi bi-pencil"></i>
        </button>
        <button
          @click="$emit('deleteLot', lot.id)"
          class="btn btn-sm btn-outline-danger"
          title="Delete"
        >
          <i class="bi bi-trash"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps(["lot"]);
</script>

<style scoped>
.lot-card {
  border-radius: 12px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.lot-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1) !important;
}

.lot-details {
  font-size: 0.9rem;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.8rem;
}
</style>
