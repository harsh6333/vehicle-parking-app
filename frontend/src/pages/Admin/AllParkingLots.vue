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
          active: true,
        },
        {
          title: 'Summary',
          link: '/admin/statistics',
          icon: 'bi bi-clock-history',
        },
        {
          title: 'Search',
          link: '/admin/search',
          icon: 'bi-search',
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
            <LotForm
              :modelValue="form"
              @submit="handleUpdate"
              @delete="handleDelete"
            />
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
  deleteLotById,
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

const handleDelete = async (lotId) => {
  error.value = "";
  try {
    await deleteLotById(lotId);
    form.value = { id: null };
    await loadLots();
  } catch (err) {
    console.error(`Update failed for lot ${lotId}`, err);
    error.value =
      err?.response?.data?.msg ||
      `Update failed for Lot ID ${lotId}. Please check the data and try again.`;
  }
};

onMounted(loadLots);
</script>
<style scoped>
@import "../../styles/allparkinglots.css";
</style>
