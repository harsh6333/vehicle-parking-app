<template>
  <div class="card border-0 shadow-sm">
    <div class="card-header bg-white border-0 py-3">
      <h5 class="mb-0">
        <i class="bi bi-clock-history me-2 text-primary"></i>
        Recent Reservations
      </h5>
    </div>
    <div class="card-body">
      <div class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Lot</th>
              <th>Spot</th>
              <th>Time Period</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="entry in history" :key="entry.id">
              <td>{{ entry.lot_name }}</td>
              <td>#{{ entry.spot_id }}</td>
              <td>
                {{ formatTime(entry.reserved_at) }} -
                {{ formatTime(entry.reserved_till) }}
              </td>
              <td>
                <span
                  class="badge"
                  :class="{
                    'bg-success': entry.leaving_timestamp,
                    'bg-warning':
                      !entry.leaving_timestamp && entry.parking_timestamp,
                    'bg-info':
                      !entry.leaving_timestamp && !entry.parking_timestamp,
                  }"
                >
                  {{
                    entry.leaving_timestamp
                      ? "Completed"
                      : entry.parking_timestamp
                      ? "Occupied"
                      : "Reserved"
                  }}
                </span>
              </td>
              <td>
                <button
                  v-if="!entry.leaving_timestamp"
                  class="btn btn-sm btn-outline-danger"
                  @click="$emit('cancel', entry.spot_id, entry.reserved_at)"
                >
                  <i class="bi bi-x-circle"></i> Cancel
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="text-end mt-3">
        <router-link
          to="/user/parking_history"
          class="btn btn-sm btn-outline-primary"
        >
          View Full History <i class="bi bi-arrow-right ms-1"></i>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  history: Array,
});

defineEmits(["cancel"]);

const formatTime = (timestamp) => {
  if (!timestamp) return "-";
  const date = new Date(timestamp);
  return date.toLocaleString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
};
</script>
