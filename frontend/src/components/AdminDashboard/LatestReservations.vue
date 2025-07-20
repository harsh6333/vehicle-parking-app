<template>
  <div class="reservations-list">
    <div
      v-for="r in reservations"
      :key="r.reservation_id"
      class="reservation-card"
    >
      <!-- Top Row: ID + Spot + User -->
      <div class="header-row">
        <div class="left-info">
          <span class="badge">#{{ r.reservation_id }}</span>
          <span class="fw-semibold">Spot #{{ r.spot_id }}</span>
        </div>
        <div class="text-muted small">User: {{ r.user_id }}</div>
      </div>

      <!-- Times: Reserved vs Actual -->
      <div class="time-row">
        <div class="time-column">
          <div class="label">
            <i class="bi bi-calendar-check me-1"></i>Reserved
          </div>
          <div class="value">
            {{ formatDate(r.reserved_at) }} → {{ formatDate(r.reserved_till) }}
          </div>
        </div>
        <div class="time-column">
          <div class="label"><i class="bi bi-clock me-1"></i>Actual</div>
          <div class="value">
            <span v-if="r.parking_timestamp">
              {{ formatDateTime(r.parking_timestamp) }}
            </span>
            <span v-else class="text-muted">Not parked</span>
            →
            <span v-if="r.leaving_timestamp">
              {{ formatDateTime(r.leaving_timestamp) }}
            </span>
            <span v-else class="text-muted">Not left</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { format } from "date-fns";

defineProps({
  reservations: Array,
});

const formatDate = (str) => format(new Date(str), "MMM dd, hh:mm a");
const formatDateTime = (str) => format(new Date(str), "hh:mm a");
</script>

<style scoped>
.reservations-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.reservation-card {
  background: white;
  border-radius: 12px;
  padding: 0.9rem 1.2rem;
  border: 1px solid #e6e6e6;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
  font-size: 0.85rem;
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.left-info {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.badge {
  background-color: #2563eb;
  color: white;
  font-size: 0.7rem;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  font-weight: 500;
}

.time-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.time-column .label {
  font-weight: 600;
  color: #333;
  margin-bottom: 0.1rem;
  display: flex;
  align-items: center;
}

.time-column .value {
  font-size: 0.83rem;
  color: #555;
}
</style>
