<template>
  <div class="user-table">
    <div class="table-responsive">
      <table class="table table-hover align-middle">
        <thead>
          <tr class="text-uppercase text-muted fs-xs letter-spacing">
            <th class="bg-transparent">User</th>
            <th class="bg-transparent">Email</th>
            <th class="bg-transparent">Role</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in nonAdminUsers" :key="user.id" class="border-top-1">
            <td>
              <div class="d-flex align-items-center gap-2">
                <div class="avatar bg-primary bg-opacity-10 text-primary">
                  {{ user.username.substring(0, 2).toUpperCase() }}
                </div>
                <div>
                  <div class="fw-medium">{{ user.username }}</div>
                </div>
              </div>
            </td>
            <td>
              <div class="text-truncate" style="max-width: 180px">
                {{ user.email }}
              </div>
            </td>
            <td>
              <span
                class="badge rounded-pill py-1 px-2"
                :class="user.is_admin ? 'bg-primary' : 'bg-secondary'"
              >
                {{ user.is_admin ? "Admin" : "User" }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
const props = defineProps({ users: Array });
const nonAdminUsers = computed(() =>
  props.users.filter((user) => !user.is_admin)
);
</script>

<style scoped>
.user-table {
  border-radius: 12px;
}

.table {
  --bs-table-bg: transparent;
  --bs-table-border-color: rgba(0, 0, 0, 0.05);
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 500;
}

.letter-spacing {
  letter-spacing: 0.5px;
}

.fs-xs {
  font-size: 0.7rem;
}

.btn-icon {
  width: 32px;
  height: 32px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
}

.btn-icon:hover {
  background-color: rgba(0, 0, 0, 0.05);
}
</style>
