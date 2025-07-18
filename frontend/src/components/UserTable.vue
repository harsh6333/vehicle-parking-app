<template>
  <div class="user-table">
    <div class="table-responsive">
      <table class="table table-hover table-sm align-middle">
        <thead class="table-light">
          <tr>
            <th>User</th>
            <th>Email</th>
            <th>Role</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>
              <div class="d-flex align-items-center gap-2">
                <div
                  class="avatar bg-primary bg-opacity-10 text-primary rounded-circle d-flex align-items-center justify-content-center"
                  style="width: 32px; height: 32px"
                >
                  {{ user.username.substring(0, 2).toUpperCase() }}
                </div>
                <span>{{ user.username }}</span>
              </div>
            </td>
            <td>{{ user.email }}</td>
            <td>
              <span
                class="badge"
                :class="user.is_admin ? 'bg-success' : 'bg-secondary'"
              >
                {{ user.is_admin ? "Admin" : "User" }}
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
  </div>
</template>

<script setup>
defineProps({ users: Array });
</script>

<style scoped>
.user-table {
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

.avatar {
  font-size: 0.75rem;
  font-weight: 500;
}

.badge {
  padding: 0.35em 0.65em;
  font-weight: 500;
}
</style>
