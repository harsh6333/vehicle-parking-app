<template>
  <div class="dashboard-container">
    <NavigationBar
      :navigation="[
        {
          title: 'Dashboard',
          link: '/user/dashboard',
          icon: 'bi bi-speedometer2',
        },
        {
          title: 'History',
          link: '/user/parking_history',
          icon: 'bi bi-clock-history',
        },
      ]"
    />
    <div class="container-fluid">
      <div class="row">
        <div class="w-100 main-content py-4">
          <DashboardHeader
            :username="userInitials.username"
            @quickReserve="autoReserve"
          />

          <StatsCards
            :active-reservations="currentReservation ? '1' : '0'"
            :available-lots="availableLotsCount"
            :history-count="history.length"
          />

          <CurrentReservation
            v-if="currentReservation"
            :reservation="currentReservation"
            @checkIn="occupySpotfunc"
            @cancel="releaseSpotfunc"
          />

          <AvailableLots
            :lots="lots"
            @reserve="reserveSpotfunc"
            @viewDetails="viewLotDetails"
          />

          <RecentHistory
            :history="history.slice(0, 5)"
            @cancel="releaseSpotfunc"
          />
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
import DashboardHeader from "@/components/UserDashboard/DashboardHeader.vue";
import StatsCards from "@/components/UserDashboard/StatCards.vue";
import CurrentReservation from "@/components/UserDashboard/CurrentReservation.vue";
import AvailableLots from "@/components/UserDashboard/AvailableLots.vue";
import RecentHistory from "@/components/UserDashboard/RecentHistory.vue";
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
// const formatTime = (timestamp) => {
//   if (!timestamp) return "-";
//   const date = new Date(timestamp);
//   return date.toLocaleString([], {
//     year: "numeric",
//     month: "short",
//     day: "numeric",
//     hour: "2-digit",
//     minute: "2-digit",
//   });
// };

const loadLots = async () => {
  const res = await getLots(selectedDate.value);
  lots.value = res.data;
};

const loadHistory = async () => {
  const res = await getHistory();
  history.value = res.data;
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
