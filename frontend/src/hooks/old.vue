<template>
  <div class="dashboard-container">
    <NavigationBar />
    <!-- Main Content -->
    <div class="container-fluid">
      <div class="row">
        <!-- Main Panel -->
        <div class="w-100 main-content py-4">
          <!-- Dashboard Header -->
          <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
              <h2 class="fw-bold mb-1">
                Welcome back, {{ userInitials.username }}
              </h2>
              <p class="text-muted mb-0">Manage your parking reservations</p>
            </div>
            <button class="btn btn-success" @click="autoReserve">
              <i class="bi bi-magic me-1"></i> Quick Reserve
            </button>
          </div>

          <!-- Stats Cards -->
          <div class="row mb-4">
            <div class="col-md-4">
              <div class="card stat-card bg-white border-0 shadow-sm">
                <div class="card-body">
                  <div class="d-flex justify-content-between">
                    <div>
                      <h6 class="text-muted mb-2">Active Reservation</h6>
                      <h3 class="mb-0">{{ currentReservation ? "1" : "0" }}</h3>
                    </div>
                    <div
                      class="icon-circle bg-primary bg-opacity-10 text-primary"
                    >
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
                      <h3 class="mb-0">{{ availableLotsCount }}</h3>
                    </div>
                    <div
                      class="icon-circle bg-success bg-opacity-10 text-success"
                    >
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
                      <h3 class="mb-0">{{ history.length }}</h3>
                    </div>
                    <div class="icon-circle bg-info bg-opacity-10 text-info">
                      <i class="bi bi-clock-history"></i>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Current Reservation -->
          <div class="card mb-4 border-0 shadow-sm" v-if="currentReservation">
            <div class="card-header bg-white border-0 py-3">
              <h5 class="mb-0">
                <i class="bi bi-car-front me-2 text-primary"></i>
                Current Reservation
              </h5>
            </div>
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <h4 class="fw-bold">{{ currentReservation.lot_name }}</h4>
                  <p class="text-muted mb-1">
                    <i class="bi bi-geo-alt me-1"></i>
                    {{ currentReservation.address }}
                  </p>
                  <div class="d-flex gap-3">
                    <div>
                      <small class="text-muted">Spot</small>
                      <p class="mb-0 fw-bold">
                        #{{ currentReservation.spot_id }}
                      </p>
                    </div>
                    <div>
                      <small class="text-muted">From</small>
                      <p class="mb-0 fw-bold">
                        {{ formatTime(currentReservation.reserved_at) }}
                      </p>
                    </div>
                    <div>
                      <small class="text-muted">To</small>
                      <p class="mb-0 fw-bold">
                        {{ formatTime(currentReservation.reserved_till) }}
                      </p>
                    </div>
                  </div>
                </div>
                <div class="d-flex gap-2">
                  <button
                    class="btn btn-outline-primary"
                    @click="
                      occupySpotfunc(
                        currentReservation.spot_id,
                        currentReservation.reserved_at
                      )
                    "
                    v-if="!currentReservation?.parking_timestamp"
                  >
                    <i class="bi bi-check-circle me-1"></i> Check In
                  </button>
                  <button
                    class="btn btn-outline-danger"
                    @click="
                      releaseSpotfunc(
                        currentReservation.spot_id,
                        currentReservation.reserved_at
                      )
                    "
                  >
                    <i class="bi bi-x-circle me-1"></i> Cancel
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Available Lots -->
          <div class="card mb-4 border-0 shadow-sm">
            <div class="card-header bg-white border-0 py-3">
              <h5 class="mb-0">
                <i class="bi bi-map me-2 text-primary"></i>
                Available Parking Lots
              </h5>
            </div>
            <div class="card-body">
              <div class="row g-4">
                <div
                  class="col-md-6 col-lg-4"
                  v-for="lot in lots"
                  :key="lot.id"
                >
                  <div class="card h-100 border-0 shadow-sm lot-card">
                    <div class="card-body">
                      <div
                        class="d-flex justify-content-between align-items-start mb-3"
                      >
                        <div>
                          <h5 class="fw-bold mb-1">
                            {{ lot.prime_location_name }}
                          </h5>
                          <p class="text-muted small mb-2">
                            <i class="bi bi-geo-alt me-1"></i>
                            {{ lot.address }}
                          </p>
                        </div>
                        <span class="badge bg-success-subtle text-success">
                          ₹{{ lot.price }}/hr
                        </span>
                      </div>

                      <div class="spot-grid">
                        <div
                          v-for="spot in lot.spots.slice(0, 6)"
                          :key="spot.spot_id"
                          class="spot-item"
                          :class="{
                            available: !spot.reservations.length,
                            reserved: spot.reservations.length,
                          }"
                          @click="
                            spot.reservations.length
                              ? null
                              : reserveSpotfunc(spot.spot_id)
                          "
                          :title="
                            spot.reservations.length
                              ? 'Reserved'
                              : 'Click to reserve'
                          "
                        >
                          #{{ spot.spot_id }}
                        </div>
                        <div
                          v-if="lot.spots.length > 6"
                          class="spot-item more-spots"
                        >
                          +{{ lot.spots.length - 6 }} more
                        </div>
                      </div>

                      <button
                        class="btn btn-outline-primary w-100 mt-3"
                        @click="viewLotDetails(lot.id)"
                      >
                        View All Spots
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Recent History -->
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
                    <tr v-for="entry in history.slice(0, 5)" :key="entry.id">
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
                              !entry.leaving_timestamp &&
                              entry.parking_timestamp,
                            'bg-info':
                              !entry.leaving_timestamp &&
                              !entry.parking_timestamp,
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
                          @click="
                            releaseSpotfunc(entry.spot_id, entry.reserved_at)
                          "
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
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useAuthStore } from "@/store/auth";
import { useRouter } from "vue-router";
import NavigationBar from "@/components/Common/NavigationBar.vue";
import {
  getLots,
  reserveSpot,
  occupySpot,
  releaseSpot,
  getHistory,
} from "@/services/userService";

const auth = useAuthStore();
const router = useRouter();
const lots = ref([]);
const currentReservation = ref(null);
const history = ref([]);
const selectedDate = ref(new Date().toISOString().split("T")[0]);

// Computed properties
const userInitials = computed(() => ({
  username: auth?.user?.username || "",
  initials: (auth.user?.username?.substring(0, 2) || "US").toUpperCase(),
}));

const availableLotsCount = computed(() => {
  return lots.value.filter((lot) =>
    lot.spots.some((spot) => !spot.reservations.length)
  ).length;
});

// Methods
const formatTime = (timestamp) => {
  if (!timestamp) return "-";
  const date = new Date(timestamp);
  return date.toLocaleString([], {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

const loadLots = async () => {
  const res = await getLots(selectedDate.value);
  lots.value = res.data;
};

const loadHistory = async () => {
  const res = await getHistory();
  history.value = res.data;
  // Set current reservation if any active
  currentReservation.value =
    history.value.find((entry) => !entry.leaving_timestamp) || null;
};

const reserveSpotfunc = async (spotId, time = "00:00", hours = 1) => {
  const [h, m] = time.split(":").map(Number);
  const start = new Date();
  start.setHours(h, m, 0, 0);

  const localTime = `${start.getFullYear()}-${(start.getMonth() + 1)
    .toString()
    .padStart(2, "0")}-${start.getDate().toString().padStart(2, "0")} ${h
    .toString()
    .padStart(2, "0")}:${m.toString().padStart(2, "0")}`;

  const res = await reserveSpot(spotId, localTime, hours);
  currentReservation.value = res.data;
  await loadLots();
  await loadHistory();
};

const autoReserve = async () => {
  for (const lot of lots.value) {
    const availableSpot = lot.spots.find((spot) => !spot.reservations.length);
    if (availableSpot) {
      await reserveSpotfunc(availableSpot.spot_id);
      return;
    }
  }
  alert("No available spots found for quick reservation.");
};

const occupySpotfunc = async (id, reserved_at) => {
  await occupySpot(id, reserved_at);
  currentReservation.value.parking_timestamp = new Date().toISOString();
  await loadHistory();
};

const releaseSpotfunc = async (id, reserved_at) => {
  await releaseSpot(id, reserved_at);
  currentReservation.value = null;
  await loadLots();
  await loadHistory();
};

const viewLotDetails = (lotId) => {
  router.push(`/lot/${lotId}`);
};

// Lifecycle
onMounted(async () => {
  await auth.fetchUser();
  await loadLots();
  await loadHistory();
});
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.main-content {
  padding: 1.5rem;
}

.nav-link {
  border-radius: 0.25rem;
  padding: 0.5rem 1rem;
  margin: 0.25rem 0;
  color: #495057;
}

.nav-link.active {
  background-color: rgba(13, 110, 253, 0.1);
  color: #0d6efd;
  font-weight: 500;
}

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

.lot-card {
  border-radius: 0.75rem;
  transition: transform 0.2s;
  border-left: 4px solid #0d6efd;
}

.lot-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1) !important;
}

.spot-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.5rem;
}

.spot-item {
  padding: 0.5rem;
  text-align: center;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

.spot-item.available {
  background-color: #e8f5e9;
  color: #2e7d32;
  border: 1px solid #c8e6c9;
}

.spot-item.available:hover {
  background-color: #c8e6c9;
}

.spot-item.reserved {
  background-color: #ffebee;
  color: #c62828;
  border: 1px solid #ffcdd2;
  cursor: not-allowed;
}

.spot-item.more-spots {
  background-color: #e3f2fd;
  color: #1565c0;
  border: 1px solid #bbdefb;
  grid-column: span 3;
}

.avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
}

.table {
  --bs-table-hover-bg: rgba(13, 110, 253, 0.05);
}

.table th {
  border-top: none;
  font-weight: 600;
  color: #6c757d;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.5px;
}
</style>
