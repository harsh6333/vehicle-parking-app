<template>
  <div class="spot-list">
    <div class="table-responsive">
      <table class="table table-hover table-sm align-middle">
        <thead class="table-light">
          <tr>
            <th>Spot ID</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="spot in spots" :key="spot.id">
            <td>
              <span class="badge bg-secondary bg-opacity-10 text-secondary">
                #{{ spot.id }}
              </span>
            </td>
            <td>
              <span
                class="badge"
                :class="spot.status === 'A' ? 'bg-success' : 'bg-danger'"
              >
                <i
                  class="bi"
                  :class="
                    spot.status === 'A' ? 'bi-check-circle' : 'bi-x-circle'
                  "
                ></i>
                {{ spot.status === "A" ? "Available" : "Occupied" }}
              </span>
            </td>
            <td>
              <button class="btn btn-sm btn-outline-secondary" title="Edit">
                <i class="bi bi-pencil"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="d-flex justify-content-between align-items-center mt-3">
      <small class="text-muted">Showing {{ spots.length }} spots</small>
      <button class="btn btn-sm btn-outline-primary">
        <i class="bi bi-plus-lg"></i> Add Spot
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({ spots: Array });
</script>

<style scoped>
.spot-list {
  background-color: white;
  border-radius: 8px;
  padding: 1rem;
}

.table {
  font-size: 0.9rem;
}

.table th {
  font-weight: 500;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.5px;
}

.badge {
  padding: 0.35em 0.65em;
  font-weight: 500;
}
</style>
