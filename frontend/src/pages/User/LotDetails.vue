<template>
  <div class="lot-details-container">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <button class="btn btn-outline-secondary" @click="goBack">
        <i class="bi bi-arrow-left"></i> Back
      </button>
      <h2 class="mb-0 text-primary">{{ lot.prime_location_name }}</h2>
      <div></div>
    </div>

    <!-- Lot Info Card -->
    <div class="card shadow-sm mb-4">
      <div class="card-body">
        <div
          class="d-flex justify-content-between align-items-center flex-wrap"
        >
          <div>
            <p class="mb-1 text-muted">
              <i class="bi bi-geo-alt"></i> {{ lot.address }}
            </p>
            <p class="mb-0 text-muted">PIN: {{ lot.pin_code }}</p>
          </div>
          <span class="badge bg-primary-subtle text-primary fs-6 py-2 px-3">
            <i class="bi bi-currency-rupee"></i> {{ lot.price }}/hour
          </span>
        </div>
      </div>
    </div>

    <!-- Legend -->
    <div class="card shadow-sm mb-4">
      <div class="card-body py-2">
        <div class="d-flex gap-4 flex-wrap align-items-center">
          <div class="d-flex align-items-center gap-2">
            <span class="availability-dot available"></span>
            <span class="small">Available</span>
          </div>
          <div class="d-flex align-items-center gap-2">
            <span class="availability-dot reserved"></span>
            <span class="small">Reserved</span>
          </div>
          <div class="d-flex align-items-center gap-2">
            <span class="availability-dot occupied"></span>
            <span class="small">Occupied</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Spots Grid -->
    <div class="spots-grid">
      <div
        v-for="spot in spots"
        :key="spot.id"
        class="card spot-card shadow-sm"
        :class="spot.status"
      >
        <div class="card-body">
          <div class="spot-number fw-bold text-primary mb-3">
            <i class="bi bi-p-square"></i> Spot #{{ spot.id }}
          </div>

          <!-- Reservation Form -->
          <div class="reservation-form">
            <div class="mb-2">
              <label class="form-label small mb-1">Start Time</label>
              <input
                type="time"
                v-model="startTimes[spot.id]"
                class="form-control form-control-sm"
              />
            </div>
            <div class="mb-3">
              <label class="form-label small mb-1">Duration (hours)</label>
              <input
                type="number"
                v-model="durations[spot.id]"
                min="1"
                step="1"
                class="form-control form-control-sm"
              />
            </div>
            <button
              class="btn btn-primary btn-sm w-100 reserve-btn"
              @click="reserveSpotfunc(spot.id)"
            >
              <i class="bi bi-calendar-plus"></i> Reserve
            </button>
          </div>

          <!-- Reservation Info -->
          <div
            v-if="spot.reservations.length"
            class="reservation-info mt-4 pt-3 border-top"
          >
            <h6 class="small text-muted mb-2">Current Reservations:</h6>
            <div
              v-for="res in spot.reservations"
              :key="res.id"
              class="reservation-item mb-3"
            >
              <div class="d-flex justify-content-between small">
                <span class="fw-semibold">From:</span>
                <span>{{ formatTime(res.reserved_at) }}</span>
              </div>
              <div class="d-flex justify-content-between small">
                <span class="fw-semibold">To:</span>
                <span>{{ formatTime(res.reserved_till) }}</span>
              </div>
              <div class="status-badge mt-2 text-center" :class="res.status">
                {{ capitalize(res.status) }}
              </div>
            </div>
          </div>
          <div
            v-else
            class="availability-text text-center mt-3 pt-3 border-top"
          >
            <i class="bi bi-check-circle-fill text-success"></i>
            <span class="small ms-1">Available all day</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { fetchSpots, reserveSpot } from "@/services/userService";

const router = useRouter();
const route = useRoute();
const lotId = route.params.id;

const lot = ref({});
const spots = ref([]);
const durations = ref({});
const startTimes = ref({});

const goBack = () => {
  router.go(-1);
};

const fetchSpotsfunc = async () => {
  try {
    const now = new Date();
    const istOffset = 5.5 * 60 * 60 * 1000;
    const istDate = new Date(now.getTime() + istOffset);

    const istDateStr = istDate.toISOString().split("T")[0];

    const response = await fetchSpots(lotId, istDateStr);
    lot.value = response.data.lot;
    spots.value = response.data.spots;
  } catch (error) {
    console.error("Error fetching spots:", error);
  }
};

const reserveSpotfunc = async (spotId) => {
  try {
    const duration = Number(durations.value[spotId] || 1);
    const timeStr = startTimes.value[spotId] || "00:00";
    const [hour, minute] = timeStr.split(":").map(Number);

    const today = new Date();
    const localStart = new Date(
      today.getFullYear(),
      today.getMonth(),
      today.getDate(),
      hour,
      minute
    );

    const start_time = localStart.toISOString();

    await reserveSpot(spotId, start_time, duration);
    await fetchSpotsfunc();
  } catch (error) {
    console.error("Error reserving spot:", error);
  }
};

const formatTime = (ts) => {
  if (!ts) return "-";
  const date = new Date(ts);
  return date.toLocaleTimeString("en-IN", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
    timeZone: "Asia/Kolkata",
  });
};

const capitalize = (text) =>
  text ? text.charAt(0).toUpperCase() + text.slice(1) : "";

onMounted(fetchSpotsfunc);
</script>

<style scoped>
.lot-details-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.spots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.spot-card {
  border-radius: 10px;
  transition: transform 0.2s, box-shadow 0.2s;
  border: none;
}

.spot-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1) !important;
}

.spot-card.available {
  border-top: 3px solid #4caf50;
}

.spot-card.reserved {
  border-top: 3px solid #ff7043;
}

.spot-card.occupied {
  border-top: 3px solid #2196f3;
}

.spot-number {
  font-size: 1.1rem;
}

.reservation-form {
  background-color: rgba(0, 0, 0, 0.02);
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.reservation-info {
  font-size: 0.85rem;
}

.reservation-item {
  background-color: rgba(0, 0, 0, 0.03);
  padding: 10px;
  border-radius: 6px;
}

.status-badge {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
  width: 100%;
}

.status-badge.reserved {
  background-color: rgba(255, 112, 67, 0.1);
  color: #e64a19;
}

.status-badge.occupied {
  background-color: rgba(33, 150, 243, 0.1);
  color: #1565c0;
}

.availability-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
}

.availability-dot.available {
  background-color: #4caf50;
}

.availability-dot.reserved {
  background-color: #ff7043;
}

.availability-dot.occupied {
  background-color: #2196f3;
}

.reserve-btn {
  font-size: 0.85rem;
  padding: 0.25rem 0.5rem;
}
</style>
