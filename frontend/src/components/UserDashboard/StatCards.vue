<template>
  <div class="row mb-4">
    <div class="col-md-4">
      <div class="card stat-card bg-white border-0 shadow-sm">
        <div class="card-body">
          <div class="d-flex justify-content-between">
            <div>
              <h6 class="text-muted mb-2">Active Reservation</h6>
              <h3 class="mb-0">{{ activeReservations }}</h3>
            </div>
            <div class="icon-circle bg-primary bg-opacity-10 text-primary">
              <i class="bi bi-calendar-check"></i>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card stat-card bg-white border-0 shadow-sm">
        <div class="card-body">
          <div class="d-flex justify-content-between">
            <div>
              <h6 class="text-muted mb-2">Available Lots</h6>
              <h3 class="mb-0">{{ availableLots }}</h3>
            </div>
            <div class="icon-circle bg-success bg-opacity-10 text-success">
              <i class="bi bi-p-square"></i>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card stat-card bg-white border-0 shadow-sm">
        <div class="card-body">
          <div class="d-flex justify-content-between">
            <div>
              <h6 class="text-muted mb-2">Reservation History</h6>
              <h3 class="mb-0">{{ historyCount }}</h3>
            </div>
            <div class="icon-circle bg-info bg-opacity-10 text-info">
              <i class="bi bi-clock-history"></i>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  activeReservations: [String, Number],
  availableLots: [String, Number],
  historyCount: [String, Number],
});
</script>

<style scoped>
.stat-card {
  border-radius: 0.75rem;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-3px);
}

.icon-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}
</style>
