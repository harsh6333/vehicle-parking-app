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
            <div class="mb-3">
              <label class="form-label small mb-1">Start Date & Time</label>

              <VueDatePicker
                v-model="dateTimes[spot.id]"
                :min-date="new Date()"
                :enable-time-picker="true"
                :enable-seconds="false"
                :is-24="false"
                auto-apply
                placeholder="Select date and time"
                :prevent-min-max-navigation="false"
                :format="'dd MMM yyyy hh:mm aa'"
                :model-auto="false"
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
  <!-- Error Toast -->
  <ErrorToast v-if="error" :message="error" @dismiss="error = null" />
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { fetchSpots, reserveSpot } from "@/services/userService";
import ErrorToast from "@/components/Common/ErrorToast.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";

// Inside setup()
// const format = ref("dd/MM/yyyy hh:mm aa");
const dateTimes = ref({});

const router = useRouter();
const route = useRoute();
const lotId = route.params.id;

const lot = ref({});
const spots = ref([]);
const durations = ref({});

const goBack = () => {
  router.go(-1);
};
const error = ref(null);

const fetchSpotsfunc = async () => {
  error.value = null;
  try {
    const now = new Date();
    const istOffset = 5.5 * 60 * 60 * 1000;
    const istDate = new Date(now.getTime() + istOffset);
    const istDateStr = istDate.toISOString().split("T")[0];

    const response = await fetchSpots(lotId, istDateStr);
    lot.value = response.data.lot;
    spots.value = response.data.spots;
  } catch (err) {
    console.error("Error fetching spots:", err);
    error.value = "Failed to load spots. Please try again later.";
  }
};

const reserveSpotfunc = async (spotId) => {
  error.value = null;
  try {
    const duration = Number(durations.value[spotId] || 1);
    const localStart = new Date(dateTimes.value[spotId]);
    const start_time = localStart.toISOString();

    await reserveSpot(spotId, start_time, duration);
    await fetchSpotsfunc();
  } catch (err) {
    console.error("Error reserving spot:", err);

    const message =
      err.response?.data?.msg ||
      err.msg ||
      "Failed to reserve the spot. Please try again.";
    error.value = message;
  }
};

const formatTime = (ts) => {
  if (!ts) return "-";
  const date = new Date(ts);
  return date.toLocaleString("en-IN", {
    year: "numeric",
    month: "short",
    day: "2-digit",
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
@import "@/styles/lotdetails.css";
</style>
