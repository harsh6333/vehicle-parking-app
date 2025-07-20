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

            <div class="timeline">
              <div class="timeline-item">
                <i class="bi bi-calendar-check"></i>
                <div>
                  <div>Reserved</div>
                  <div class="time">
                    {{ formatDateTime(record.reserved_at) }}
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
                        ? formatDateTime(record.parking_timestamp)
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
                        ? formatDateTime(record.leaving_timestamp)
                        : "Not left"
                    }}
                  </div>
                </div>
              </div>
            </div>

            <div class="duration" v-if="record.duration_minutes">
              <i class="bi bi-clock"></i>
              {{ Math.round(record.duration_minutes) }} minutes
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
import { format } from "date-fns";

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

const formatDate = (dateStr) => {
  return format(new Date(dateStr), "MMM dd, yyyy");
};

const formatDateTime = (dateStr) => {
  return format(new Date(dateStr), "MMM dd, hh:mm a");
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
}

.date {
  font-size: 0.85rem;
  color: #6c757d;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
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
}

.timeline-item div div:first-child {
  font-weight: 500;
  font-size: 0.9rem;
}

.time {
  font-size: 0.85rem;
  color: #6c757d;
}

.duration {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: var(--bs-success);
  font-weight: 500;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
