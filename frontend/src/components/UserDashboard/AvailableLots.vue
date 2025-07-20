<template>
  <div class="card mb-4 border-0 shadow-sm">
    <div class="card-header bg-white border-0 py-3">
      <h5 class="mb-0">
        <i class="bi bi-map me-2 text-primary"></i>
        Available Parking Lots
      </h5>
    </div>
    <div class="card-body">
      <div class="row g-4">
        <div class="col-md-6 col-lg-4" v-for="lot in lots" :key="lot.id">
          <LotCard
            :lot="lot"
            @view-details="(lotId) => $emit('viewDetails', lotId)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import LotCard from "./LotCard.vue";

defineProps({
  lots: Array,
});

defineEmits(["viewDetails"]);
</script>
