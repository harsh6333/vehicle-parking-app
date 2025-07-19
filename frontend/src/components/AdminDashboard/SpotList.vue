<template>
  <div class="spot-list card shadow-sm border-0">
    <div
      class="card-header bg-white d-flex justify-content-between align-items-center"
    >
      <h5 class="mb-0">
        <i class="bi bi-car-front me-2 text-primary"></i>
        Parking Spots
      </h5>

      <input
        type="date"
        :value="date"
        class="form-control form-control-sm w-auto"
        @change="$emit('dateChange', $event.target.value)"
      />
    </div>

    <div class="card-body p-0">
      <div class="table-responsive">
        <table class="table table-hover table-sm align-middle mb-0">
          <thead class="table-light">
            <tr>
              <th>Spot ID</th>
              <th>Status</th>
              <th>Reservations ({{ date }})</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="spot in spots" :key="spot.spot_id">
              <td>#{{ spot.spot_id }}</td>
              <td>
                <span
                  class="badge"
                  :class="
                    spot.reservations.length === 0
                      ? 'bg-success'
                      : 'bg-warning text-dark'
                  "
                >
                  {{
                    spot.reservations.length === 0 ? "Available" : "Reserved"
                  }}
                </span>
              </td>
              <td>
                <div v-if="spot.reservations.length">
                  <div
                    v-for="res in spot.reservations"
                    :key="res.reservation_id"
                    class="mb-1 text-muted small"
                  >
                    <i class="bi bi-clock me-1"></i>
                    {{ formatTime(res.reserved_at) }} →
                    {{ formatTime(res.reserved_till) }}
                    <span class="badge bg-light text-dark ms-2"
                      >User #{{ res.user_id }}</span
                    >
                  </div>
                </div>
                <div v-else class="text-muted">No reservations</div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="px-3 py-2 border-top text-end text-muted small">
        Showing {{ spots.length }} spots
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  spots: Array,
  date: String,
});

const formatTime = (datetimeStr) => {
  const date = new Date(datetimeStr);
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
};
</script>
