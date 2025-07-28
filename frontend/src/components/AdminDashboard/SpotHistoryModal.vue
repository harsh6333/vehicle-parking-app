<template>
  <div class="spot-history-modal" v-if="visible" @click.self="close">
    <div class="modal-content">
      <div class="modal-header">
        <h3>Booking History for Spot #{{ spotId }}</h3>
        <button @click="close" class="close-btn">
          <i class="bi bi-x-lg"></i>
        </button>
      </div>

      <div class="modal-body">
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading history...</p>
        </div>

        <div v-else-if="history.length === 0" class="empty-state">
          <i class="bi bi-clock-history"></i>
          <p>No booking history found for this spot</p>
        </div>

        <div v-else class="history-list">
          <div
            v-for="record in history"
            :key="record.reservation_id"
            class="history-item"
          >
            <div class="history-header">
              <span class="badge" :class="getStatusClass(record.status)">
                {{ record.status }}
              </span>
              <span class="date">{{ formatDate(record.reserved_at) }}</span>
            </div>

            <div class="user-info">
              <div class="avatar">
                {{ record.username.substring(0, 2).toUpperCase() }}
              </div>
              <div>
                <div class="username">{{ record.username }}</div>
                <div class="email">{{ record.email }}</div>
              </div>
            </div>

            <div class="vehicle-details">
              <div class="detail-row">
                <span class="detail-label">Vehicle:</span>
                <span class="detail-value">{{
                  record.vehicle.vehicle_number
                }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Type:</span>
                <span class="detail-value">{{
                  record.vehicle.vehicle_type
                }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Brand/Color:</span>
                <span class="detail-value"
                  >{{ record.vehicle.brand }} ({{ record.vehicle.color }})</span
                >
              </div>
            </div>

            <div class="timeline">
              <div class="timeline-item">
                <i class="bi bi-calendar-check"></i>
                <div>
                  <div>Reserved</div>
                  <div class="time">
                    {{ formatDateTimeIST(record.reserved_at) }}
                  </div>
                  <div class="time-duration">
                    Reserved till: {{ formatDateTimeIST(record.reserved_till) }}
                  </div>
                </div>
              </div>

              <div class="timeline-item">
                <i class="bi bi-car-front"></i>
                <div>
                  <div>Parked</div>
                  <div class="time">
                    {{
                      record.parking_timestamp
                        ? formatDateTimeIST(record.parking_timestamp)
                        : "Not parked"
                    }}
                  </div>
                </div>
              </div>

              <div class="timeline-item">
                <i class="bi bi-box-arrow-right"></i>
                <div>
                  <div>Left</div>
                  <div class="time">
                    {{
                      record.leaving_timestamp
                        ? formatDateTimeIST(record.leaving_timestamp)
                        : "Not left"
                    }}
                  </div>
                </div>
              </div>
            </div>

            <div class="duration" v-if="record.duration_minutes">
              <i class="bi bi-clock"></i>
              {{ formatDuration(record.duration_minutes) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import { fetchSpotHistory } from "@/services/adminService";
import { format, addHours } from "date-fns";

const props = defineProps({
  spotId: Number,
  visible: Boolean,
});

const emit = defineEmits(["close"]);
const history = ref([]);
const loading = ref(false);

watch(
  () => props.visible,
  async (visible) => {
    if (visible) {
      await loadHistory();
    }
  }
);

const loadHistory = async () => {
  loading.value = true;
  try {
    const response = await fetchSpotHistory(props.spotId);
    history.value = response.data.history || [];
  } catch (error) {
    console.error("Failed to load spot history:", error);
  } finally {
    loading.value = false;
  }
};

const close = () => {
  emit("close");
};

const toIST = (dateStr) => {
  if (!dateStr) return null;
  const date = new Date(dateStr);
  return addHours(date, 5.5); // Convert UTC to IST (UTC+5:30)
};

const formatDate = (dateStr) => {
  const date = toIST(dateStr);
  return format(date, "MMM dd, yyyy");
};

const formatDateTimeIST = (dateStr) => {
  if (!dateStr) return "N/A";
  const date = toIST(dateStr);
  return format(date, "MMM dd, hh:mm a");
};

const formatDuration = (minutes) => {
  if (minutes < 60) {
    return `${Math.round(minutes)} minutes`;
  }
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = Math.round(minutes % 60);
  if (hours < 24) {
    return `${hours} hour${hours !== 1 ? "s" : ""}${
      remainingMinutes > 0 ? ` ${remainingMinutes} min` : ""
    }`;
  }
  const days = Math.floor(hours / 24);
  const remainingHours = hours % 24;
  return `${days} day${days !== 1 ? "s" : ""}${
    remainingHours > 0
      ? ` ${remainingHours} hr${remainingHours !== 1 ? "s" : ""}`
      : ""
  }`;
};

const getStatusClass = (status) => {
  return (
    {
      Completed: "bg-success",
      "In Progress": "bg-primary",
      Reserved: "bg-warning",
    }[status] || "bg-secondary"
  );
};

onMounted(() => {
  loadHistory();
});
</script>

<style scoped>
.spot-history-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.25rem;
  color: #6c757d;
  cursor: pointer;
}

.modal-body {
  padding: 1.5rem;
}

.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  gap: 1rem;
}

.spinner {
  width: 3rem;
  height: 3rem;
  border: 0.25rem solid rgba(0, 0, 0, 0.1);
  border-top-color: var(--bs-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.empty-state i {
  font-size: 2rem;
  color: var(--bs-gray-400);
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.history-item {
  border: 1px solid #eee;
  border-radius: 10px;
  padding: 1.25rem;
  background: #f9f9f9;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.badge {
  padding: 0.35rem 0.65rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
  color: white;
}

.date {
  font-size: 0.85rem;
  color: #6c757d;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(var(--bs-primary-rgb), 0.1);
  color: var(--bs-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
}

.username {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.email {
  font-size: 0.85rem;
  color: #6c757d;
}

.vehicle-details {
  background: #f0f0f0;
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.detail-row {
  display: flex;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.detail-row:last-child {
  margin-bottom: 0;
}

.detail-label {
  font-weight: 500;
  min-width: 100px;
  color: #555;
}

.detail-value {
  color: #333;
}

.timeline {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
}

.timeline-item {
  display: flex;
  gap: 1rem;
}

.timeline-item i {
  color: var(--bs-primary);
  font-size: 1.25rem;
  margin-top: 2px;
}

.timeline-item div div:first-child {
  font-weight: 500;
  font-size: 0.9rem;
}

.time {
  font-size: 0.85rem;
  color: #6c757d;
}

.time-duration {
  font-size: 0.8rem;
  color: #888;
  margin-top: 0.25rem;
  font-style: italic;
}

.duration {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: var(--bs-success);
  font-weight: 500;
  padding-top: 0.5rem;
  border-top: 1px solid #eee;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
