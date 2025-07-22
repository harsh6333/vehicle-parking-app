<template>
  <div class="card border-0 shadow-sm">
    <div
      class="card-header bg-white border-0 py-3 d-flex justify-content-between"
    >
      <h5 class="mb-0">Your Reservations</h5>
      <button class="btn btn-sm btn-outline-primary" @click="$emit('export')">
        <i class="bi bi-download me-1"></i> Export
      </button>
    </div>

    <div class="card-body p-0">
      <div v-if="history.length === 0" class="text-center py-5">
        <i class="bi bi-clock-history text-muted" style="font-size: 3rem"></i>
        <h5 class="mt-3">No reservations found</h5>
        <p class="text-muted">You don't have any reservation history yet</p>
        <router-link to="/user/dashboard" class="btn btn-primary mt-2">
          <i class="bi bi-car-front me-1"></i> Find Parking
        </router-link>
      </div>

      <div v-else class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-light">
            <tr>
              <th>Date</th>
              <th>Location</th>
              <th>Spot</th>
              <th>Time Slot</th>
              <th>Duration</th>
              <th>Status</th>
              <th>Amount</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="entry in history" :key="entry.id">
              <td>
                <div class="fw-semibold">
                  {{ formatDate(entry.reserved_at) }}
                </div>
                <small class="text-muted">{{
                  formatDay(entry.reserved_at)
                }}</small>
              </td>
              <td>
                <div>{{ entry.lot_name }}</div>
                <small class="text-muted">{{ entry.address }}</small>
              </td>
              <td class="fw-semibold">#{{ entry.spot_id }}</td>
              <td>
                <div
                  class="d-flex gap-2 align-items-center justify-content-center"
                >
                  <span>{{ formatTime(entry.reserved_at) }}</span>
                  <span class="text-muted small">to</span>
                  <span>{{ formatTime(entry.reserved_till) }}</span>
                </div>
              </td>
              <td class="fw-semibold">
                {{ calculateDuration(entry.reserved_at, entry.reserved_till) }}h
              </td>
              <td>
                <span class="badge rounded-pill" :class="getStatusClass(entry)">
                  <i :class="getStatusIcon(entry)" class="me-1"></i>
                  {{ getStatusText(entry) }}
                </span>
              </td>
              <td class="fw-semibold">₹{{ calculateAmount(entry) }}</td>
              <td>
                <button
                  v-if="!entry.leaving_timestamp"
                  class="btn btn-sm btn-outline-danger"
                  @click="$emit('cancel', entry.id, entry.reserved_at)"
                  title="Cancel Reservation"
                >
                  <i class="bi bi-x-circle"></i>
                </button>
                <button
                  v-else
                  class="btn btn-sm btn-outline-secondary"
                  disabled
                  title="Completed"
                >
                  <i class="bi bi-check-circle"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <div
          class="d-flex justify-content-between align-items-center p-3 border-top"
        >
          <div class="text-muted small">
            Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to
            {{ Math.min(currentPage * itemsPerPage, totalItems) }} of
            {{ totalItems }} entries
          </div>
          <nav>
            <ul class="pagination mb-0">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <button class="page-link" @click="$emit('prevPage')">
                  <i class="bi bi-chevron-left"></i>
                </button>
              </li>
              <li
                v-for="page in pages"
                :key="page"
                class="page-item"
                :class="{ active: page === currentPage }"
              >
                <button class="page-link" @click="$emit('goToPage', page)">
                  {{ page }}
                </button>
              </li>
              <li
                class="page-item"
                :class="{ disabled: currentPage === totalPages }"
              >
                <button class="page-link" @click="$emit('nextPage')">
                  <i class="bi bi-chevron-right"></i>
                </button>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineEmits, defineProps } from "vue";

defineProps([
  "history",
  "currentPage",
  "totalItems",
  "itemsPerPage",
  "totalPages",
  "pages",
]);
defineEmits(["cancel", "export", "prevPage", "nextPage", "goToPage"]);

function formatDate(date) {
  return new Date(date).toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

function formatDay(date) {
  return new Date(date).toLocaleDateString("en-IN", { weekday: "long" });
}

function formatTime(date) {
  return new Date(date).toLocaleTimeString("en-IN", {
    hour: "2-digit",
    minute: "2-digit",
  });
}

function calculateDuration(start, end) {
  const diff = (new Date(end) - new Date(start)) / 3600000;
  return Math.round(diff * 10) / 10;
}

function calculateAmount(entry) {
  const rate = entry.rate_per_hour || 20; // fallback if not present
  return Math.round(
    calculateDuration(entry.reserved_at, entry.reserved_till) * rate
  );
}

function getStatusClass(entry) {
  if (entry.leaving_timestamp) return "bg-success text-white";
  if (new Date(entry.reserved_till) < new Date())
    return "bg-secondary text-white";
  return "bg-warning text-dark";
}

function getStatusIcon(entry) {
  if (entry.leaving_timestamp) return "bi bi-check-circle";
  if (new Date(entry.reserved_till) < new Date()) return "bi bi-clock";
  return "bi bi-hourglass-split";
}

function getStatusText(entry) {
  if (entry.leaving_timestamp) return "Completed";
  if (new Date(entry.reserved_till) < new Date()) return "Expired";
  return "Upcoming";
}
</script>
