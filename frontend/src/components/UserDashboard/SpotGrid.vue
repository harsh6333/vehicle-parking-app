<template>
  <div class="spot-grid">
    <div
      v-for="spot in spots.slice(0, 6)"
      :key="spot.spot_id"
      class="spot-item"
      :class="{
        available: !spot.reservations.length,
        reserved: spot.reservations.length,
      }"
      :title="spot.reservations.length ? 'Reserved' : 'Click to reserve'"
    >
      #{{ spot.spot_id }}
    </div>
    <div v-if="spots.length > 6" class="spot-item more-spots">
      +{{ spots.length - 6 }} more
    </div>
  </div>
</template>

<script setup>
defineProps({
  spots: Array,
});
</script>

<style scoped>
.spot-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.5rem;
}

.spot-item {
  padding: 0.5rem;
  text-align: center;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

.spot-item.available {
  background-color: #e8f5e9;
  color: #2e7d32;
  border: 1px solid #c8e6c9;
}

.spot-item.available:hover {
  background-color: #c8e6c9;
}

.spot-item.reserved {
  background-color: #ffebee;
  color: #c62828;
  border: 1px solid #ffcdd2;
  cursor: not-allowed;
}

.spot-item.more-spots {
  background-color: #e3f2fd;
  color: #1565c0;
  border: 1px solid #bbdefb;
  grid-column: span 3;
}
</style>
