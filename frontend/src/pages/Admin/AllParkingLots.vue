<template>
  <div class="admin-dashboard">
    <NavigationBar
      :navigation="[
        {
          title: 'Dashboard',
          link: '/admin/dashboard',
          icon: 'bi bi-speedometer2',
        },
        {
          title: 'All Users',
          link: '/admin/all_users',
          icon: 'bi bi-clock-history',
        },
        {
          title: 'All Lots',
          link: '/admin/all_lots',
          icon: 'bi bi-clock-history',
        },
        {
          title: 'Summary',
          link: '/admin/statistics',
          icon: 'bi bi-clock-history',
        },
      ]"
    />

    <div class="dashboard-container">
      <!-- Loading State -->
      <div v-if="loading" class="loading-overlay">
        <div class="loading-content">
          <div class="spinner"></div>
          <p class="loading-text">Loading parking lots...</p>
        </div>
      </div>

      <!-- Main Content -->
      <div v-else class="dashboard-content">
        <!-- Header Section -->
        <div class="dashboard-header">
          <div class="stats-card">
            <div class="stat-item">
              <i class="bi bi-p-square-fill stat-icon"></i>
              <div>
                <span class="stat-value">{{ lots.length }}</span>
                <span class="stat-label">Total Lots</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Parking Lots Grid -->
        <div class="lots-grid">
          <LotCard
            v-for="lot in lots"
            :key="lot.id"
            :lot="lot"
            :is-expanded="expandedLotId === lot.id"
            :spots="expandedLotId === lot.id ? spots : []"
            @viewSpots="handleViewSpots"
            @editLot="editLot"
            class="lot-card-item"
          />
        </div>
      </div>

      <!-- Edit Form Slide Panel -->
      <transition name="slide-panel">
        <div v-if="form.id !== null" class="edit-panel">
          <div class="panel-header">
            <h3>Edit Parking Lot</h3>
            <button @click="form.id = null" class="panel-close">
              <i class="bi bi-x-lg"></i>
            </button>
          </div>
          <div class="panel-content">
            <LotForm :modelValue="form" @submit="handleUpdate" />
          </div>
        </div>
      </transition>
    </div>
  </div>
  <!-- Error Toast -->
  <ErrorToast v-if="error" :message="error" @dismiss="error = null" />
</template>

<script setup>
import LotCard from "@/components/AdminDashboard/AllLots.vue";
import LotForm from "@/components/AdminDashboard/LotForm.vue";
import ErrorToast from "@/components/Common/ErrorToast.vue";
import NavigationBar from "@/components/Common/NavigationBar.vue";
import {
  fetchLots,
  fetchSpotsForNow,
  updateLot,
} from "@/services/adminService";
import { ref, onMounted } from "vue";

const lots = ref([]);
const loading = ref(false);
const spots = ref([]);
const error = ref(null);
const expandedLotId = ref(null);
const form = ref({ id: null });

const loadLots = async () => {
  loading.value = true;
  error.value = "";
  try {
    const res = await fetchLots();
    lots.value = res.data;
  } catch (err) {
    console.error("Failed to load lots", err);
    error.value =
      err?.response?.data?.msg ||
      "Failed to load parking lots. Please try again.";
  } finally {
    loading.value = false;
  }
};

const handleViewSpots = async (lotId) => {
  error.value = "";
  try {
    if (expandedLotId.value === lotId) {
      expandedLotId.value = null;
      return;
    }
    expandedLotId.value = lotId;

    const res = await fetchSpotsForNow(lotId);
    spots.value = res.data.spots;
  } catch (err) {
    console.error(`Failed to fetch spots for lot ${lotId}`, err);
    error.value =
      err?.response?.data?.msg ||
      `Could not fetch spots for Lot ID ${lotId}. Please try again.`;
  }
};

const editLot = (lot) => {
  form.value = { ...lot };
  error.value = "";
};

const handleUpdate = async (updatedLot) => {
  error.value = "";
  try {
    await updateLot(updatedLot.id, updatedLot);
    form.value = { id: null };
    await loadLots();
  } catch (err) {
    console.error(`Update failed for lot ${updatedLot.id}`, err);
    error.value =
      err?.response?.data?.msg ||
      `Update failed for Lot ID ${updatedLot.id}. Please check the data and try again.`;
  }
};

onMounted(loadLots);
</script>
<style scoped>
.admin-dashboard {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f8fafc;
}

.dashboard-container {
  flex: 1;
  padding: 2rem;
  position: relative;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.loading-content {
  text-align: center;
}

.spinner {
  width: 3.5rem;
  height: 3.5rem;
  border: 0.35rem solid rgba(var(--bs-primary-rgb), 0.1);
  border-top-color: var(--bs-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

.loading-text {
  font-size: 1.1rem;
  color: var(--bs-dark);
  font-weight: 500;
}

.dashboard-content {
  max-width: 1440px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2.5rem;
  gap: 2rem;
}

.header-content {
  flex: 1;
}

.dashboard-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.dashboard-subtitle {
  font-size: 1rem;
  color: #64748b;
  margin: 0;
}

.stats-card {
  background: white;
  border-radius: 12px;
  padding: 1.25rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  min-width: 220px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  font-size: 1.5rem;
  color: var(--bs-primary);
  background: rgba(var(--bs-primary-rgb), 0.1);
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  display: block;
  line-height: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: #64748b;
  display: block;
  margin-top: 0.25rem;
}

.lots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 1.75rem;
}

/* Edit Panel Styles */
.edit-panel {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: 480px;
  background: white;
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.08);
  z-index: 100;
  display: flex;
  flex-direction: column;
}

.panel-header {
  padding: 1.5rem;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.panel-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  color: #1e293b;
}

.panel-close {
  background: none;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.panel-close:hover {
  background: #f1f5f9;
  color: #475569;
}

.panel-content {
  padding: 1.5rem;
  flex: 1;
  overflow-y: auto;
}

/* Animation */
.slide-panel-enter-active,
.slide-panel-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-panel-enter-from,
.slide-panel-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive Adjustments */
@media (max-width: 1024px) {
  .dashboard-header {
    flex-direction: column;
  }

  .stats-card {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 1.5rem;
  }

  .lots-grid {
    grid-template-columns: 1fr;
  }

  .edit-panel {
    width: 100%;
  }
}
</style>
