<template>
  <div>
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
          active: true,
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
        {
          title: 'Search',
          link: '/admin/search',
          icon: 'bi-search',
        },
      ]"
    />

    <div class="container mt-4">
      <h4 class="mb-3">User Summary</h4>

      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
      </div>

      <div v-else>
        <div v-if="users.length === 0" class="alert alert-info">
          No users found.
        </div>

        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-3">
          <div v-for="user in users" :key="user.email" class="col">
            <div class="card shadow-sm h-100">
              <div class="card-body">
                <h5 class="card-title">{{ user.username }}</h5>
                <p class="card-text mb-1">
                  <strong>Email:</strong> {{ user.email }}
                </p>
                <p class="card-text mb-1">
                  <strong>Reservations:</strong> {{ user.total_reservations }}
                </p>
                <p class="card-text mb-1">
                  <strong>Total Hours Parked:</strong>
                  {{ user.total_parked_hours }}
                </p>
                <p class="card-text mb-0">
                  <strong>Total Cost:</strong> ₹{{ user.total_parking_cost }}
                </p>
                <span class="badge bg-success mt-2" v-if="user.is_admin"
                  >Admin</span
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- Error Toast -->
  <ErrorToast v-if="error" :message="error" @dismiss="error = null" />
</template>

<script setup>
import ErrorToast from "@/components/Common/ErrorToast.vue";
import NavigationBar from "@/components/Common/NavigationBar.vue";
import { fetchUsers } from "@/services/adminService";
import { ref, onMounted } from "vue";

const users = ref([]);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  error.value = null;
  loading.value = true;
  try {
    const res = await fetchUsers();
    users.value = res.data;
  } catch (err) {
    console.error("Failed to fetch users", err);
    error.value =
      err?.response?.data?.msg || "Failed to load users. Please try again.";
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.card-title {
  font-weight: 600;
}
</style>
