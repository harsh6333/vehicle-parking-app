<template>
  <div class="card mb-4 border-0 shadow-sm" v-if="reservation">
    <div class="card-header bg-white border-0 py-3">
      <h5 class="mb-0">
        <i class="bi bi-car-front me-2 text-primary"></i>
        Current Reservation
      </h5>
    </div>
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h4 class="fw-bold">{{ reservation.lot_name }}</h4>
          <p class="text-muted mb-1">
            <i class="bi bi-geo-alt me-1"></i>
            {{ reservation.address }}
          </p>
          <div class="d-flex gap-3">
            <div>
              <small class="text-muted">Spot</small>
              <p class="mb-0 fw-bold">#{{ reservation.spot_id }}</p>
            </div>
            <div>
              <small class="text-muted">From</small>
              <p class="mb-0 fw-bold">
                {{ formatTime("at", reservation.reserved_at) }}
              </p>
            </div>
            <div>
              <small class="text-muted">To</small>
              <p class="mb-0 fw-bold">
                {{ formatTime("till", reservation.reserved_till) }}
              </p>
            </div>
          </div>
        </div>
        <div class="d-flex gap-2">
          <button
            class="btn btn-outline-primary"
            @click="
              $emit('checkIn', reservation.spot_id, reservation.reserved_at)
            "
            v-if="!reservation?.parking_timestamp"
          >
            <i class="bi bi-check-circle me-1"></i> Check In
          </button>
          <button
            class="btn btn-outline-danger"
            @click="
              $emit('cancel', reservation.spot_id, reservation.reserved_at)
            "
          >
            <i class="bi bi-x-circle me-1"></i> Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  reservation: Object,
});

defineEmits(["checkIn", "cancel"]);
const formatTime = (value, timestamp) => {
  if (!timestamp) return "-";

  // Remove trailing whitespace or carriage return
  timestamp = timestamp.trim();

  const [datePart, timePart] = timestamp.split("T");
  const [year, month, day] = datePart.split("-").map(Number);
  const [hour, minute] = timePart.split(":").map(Number);

  const date = new Date(year, month - 1, day, hour, minute);

  if (isNaN(date)) return "Invalid Date";

  return date.toLocaleString([], {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};
</script>
