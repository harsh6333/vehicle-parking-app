<template>
  <div class="lot-card" :class="{ expanded: isExpanded }">
    <div class="card-header">
      <div class="location-info">
        <div class="location-icon">
          <i class="bi bi-geo-alt-fill"></i>
        </div>
        <div>
          <h3 class="location-name">{{ lot.prime_location_name }}</h3>
          <div class="location-stats">
            <span class="spots-count">
              <i class="bi bi-p-circle"></i> {{ lot.total_spots }} spots
            </span>
            <span class="price-rate">
              <i class="bi bi-currency-rupee"></i> {{ lot.price }}/hr
            </span>
          </div>
        </div>
      </div>
    </div>

    <div class="card-body">
      <div class="location-details">
        <p class="address"><i class="bi bi-geo"></i> {{ lot.address }}</p>
        <p class="pin-code">
          <i class="bi bi-postcard"></i> {{ lot.pin_code }}
        </p>
      </div>

      <div v-if="isExpanded" class="spots-section">
        <div class="section-header">
          <h4>Current Spot Status</h4>
          <span class="updated-time">Updated just now</span>
        </div>

        <div class="spots-list">
          <div
            v-for="spot in spots"
            :key="spot.spot_id"
            @click="handleSpotClick(spot.spot_id)"
            class="spot-item"
          >
            <span class="spot-number">#{{ spot.spot_id }}</span>
            <span class="spot-status" :class="spot.status.toLowerCase()">
              {{ formatStatus(spot) }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div class="card-footer">
      <button class="view-btn" @click="$emit('viewSpots', lot.id)">
        <i class="bi" :class="isExpanded ? 'bi-chevron-up' : 'bi-eye'"></i>
        {{ isExpanded ? "Collapse" : "View Spots" }}
      </button>
      <button class="edit-btn" @click="$emit('editLot', lot)">
        <i class="bi bi-pencil-square"></i> Edit
      </button>
    </div>
  </div>
  <SpotHistoryModal
    v-if="showHistoryModal"
    :spot-id="selectedSpotId"
    :visible="showHistoryModal"
    @close="showHistoryModal = false"
  />
</template>

<script setup>
import { ref } from "vue";
import SpotHistoryModal from "./SpotHistoryModal.vue";

defineProps(["lot", "spots", "isExpanded"]);
defineEmits(["viewSpots", "editLot"]);

const formatTime = (str) => {
  const date = new Date(str);
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
};

const formatStatus = (spot) => {
  return spot.status === "Available"
    ? "Available"
    : `Reserved ${formatTime(spot.reservation.reserved_at)}-${formatTime(
        spot.reservation.reserved_till
      )}`;
};
const showHistoryModal = ref(false);
const selectedSpotId = ref(null);

const handleSpotClick = (spotId) => {
  selectedSpotId.value = spotId;
  showHistoryModal.value = true;
};
</script>

<style scoped>
.lot-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.lot-card.expanded {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.card-header {
  padding: 1.25rem;
  background: linear-gradient(135deg, rgba(var(--bs-primary-rgb), 0.03), white);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.location-info {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.location-icon {
  background: rgba(var(--bs-primary-rgb), 0.1);
  color: var(--bs-primary);
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  flex-shrink: 0;
}

.location-name {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 0.25rem 0;
  color: var(--bs-dark);
}

.location-stats {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: var(--bs-gray-600);
}

.spots-count,
.price-rate {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.card-body {
  padding: 1.25rem;
  flex-grow: 1;
}

.location-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: var(--bs-gray-700);
}

.address,
.pin-code {
  margin: 0;
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

.address i,
.pin-code i {
  color: var(--bs-primary);
  margin-top: 0.15rem;
}

.spots-section {
  margin-top: 1.5rem;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h4 {
  font-size: 0.95rem;
  font-weight: 600;
  margin: 0;
  color: var(--bs-dark);
}

.updated-time {
  font-size: 0.75rem;
  color: var(--bs-gray-500);
}

.spots-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.spot-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: var(--bs-gray-100);
  border-radius: 8px;
}

.spot-number {
  font-weight: 500;
  font-size: 0.9rem;
}

.spot-status {
  font-size: 0.8rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-weight: 500;
}

.spot-status.available {
  background: rgba(var(--bs-success-rgb), 0.1);
  color: var(--bs-success);
}

.spot-status.reserved {
  background: rgba(var(--bs-warning-rgb), 0.1);
  color: var(--bs-warning);
}

.card-footer {
  display: flex;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.view-btn,
.edit-btn {
  flex: 1;
  padding: 0.5rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.view-btn {
  background: rgba(var(--bs-primary-rgb), 0.05);
  color: var(--bs-primary);
  border: none;
}

.view-btn:hover {
  background: rgba(var(--bs-primary-rgb), 0.1);
}

.edit-btn {
  background: white;
  color: var(--bs-gray-700);
  border: 1px solid var(--bs-gray-300);
}

.edit-btn:hover {
  background: var(--bs-gray-100);
  border-color: var(--bs-gray-400);
}
</style>
