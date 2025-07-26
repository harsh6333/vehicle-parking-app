<script setup>
import { ref } from "vue";
import { searchLots, searchSpots, searchUsers } from "@/services/adminService";
import NavigationBar from "@/components/Common/NavigationBar.vue";
import ErrorToast from "@/components/Common/ErrorToast.vue";

const query = ref("");
const status = ref("available");
const lotId = ref("");
const result = ref([]);
const type = ref("lots");
const isLoading = ref(false);
const error = ref(null);

const runSearch = async () => {
  isLoading.value = true;
  error.value = null;
  result.value = [];

  try {
    if (type.value === "lots") {
      const res = await searchLots(query.value);
      result.value = res.data.results || res.data;
    } else if (type.value === "spots") {
      const res = await searchSpots(status.value, lotId.value || null);
      result.value = res.data;
    } else if (type.value === "users") {
      const res = await searchUsers(query.value);
      result.value = res.data.results || res.data;
    }
  } catch (err) {
    console.error("Search error:", err);
    error.value = err?.response?.data?.msg || "Search failed.";
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="">
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
        {
          title: 'Search',
          link: '/admin/search',
          icon: 'bi-search',
          active: true,
        },
      ]"
    />

    <div class="container py-4">
      <h4 class="mb-3">Admin Search</h4>

      <div class="row g-3 align-items-center">
        <div class="col-md-3">
          <select v-model="type" class="form-select">
            <option value="lots">Search Parking Lots</option>
            <option value="spots">Search Spots</option>
            <option value="users">Search Users</option>
          </select>
        </div>

        <div v-if="type === 'spots'" class="col-md-2">
          <select v-model="status" class="form-select">
            <option value="available">Available</option>
            <option value="occupied">Occupied</option>
          </select>
        </div>

        <div v-if="type === 'spots'" class="col-md-2">
          <input
            v-model="lotId"
            type="number"
            class="form-control"
            placeholder="Lot ID (optional)"
          />
        </div>

        <div v-if="type !== 'spots'" class="col-md-4">
          <input
            v-model="query"
            type="text"
            class="form-control"
            placeholder="Enter search query"
          />
        </div>

        <div class="col-md-2">
          <button @click="runSearch" class="btn btn-primary w-100">
            <i class="bi-search"></i> Search
          </button>
        </div>
      </div>

      <div class="mt-4">
        <div v-if="isLoading" class="text-center py-4">
          <div class="spinner-border text-primary"></div>
        </div>

        <div v-else>
          <h6 v-if="result.length">{{ result.length }} result(s) found</h6>
          <div v-if="!result.length && !isLoading" class="text-muted">
            No results found.
          </div>

          <div class="table-responsive mt-3" v-if="result.length">
            <table class="table table-bordered table-sm">
              <thead>
                <tr v-if="type === 'lots'">
                  <th>ID</th>
                  <th>Location</th>
                  <th>Pincode</th>
                  <th>Price (₹)</th>
                  <th>Total Spots</th>
                </tr>
                <tr v-else-if="type === 'spots'">
                  <th>ID</th>
                  <th>Lot ID</th>
                  <th>Address</th>
                  <th>Status</th>
                </tr>
                <tr v-else>
                  <th>ID</th>
                  <th>Username</th>
                  <th>Email</th>
                  <th>Admin?</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in result" :key="item.id">
                  <template v-if="type === 'lots'">
                    <td>{{ item.id }}</td>
                    <td>{{ item.prime_location_name }}</td>
                    <td>{{ item.pin_code }}</td>
                    <td>{{ item.price }}</td>
                    <td>{{ item.total_spots }}</td>
                  </template>
                  <template v-else-if="type === 'spots'">
                    <td>{{ item.id }}</td>
                    <td>{{ item.lot_id }}</td>
                    <td>{{ item.location }}</td>
                    <td>
                      <span
                        :class="{
                          'badge bg-success': item.status === 'available',
                          'badge bg-danger': item.status === 'occupied',
                        }"
                      >
                        {{ item.status }}
                      </span>
                    </td>
                  </template>
                  <template v-else>
                    <td>{{ item.id }}</td>
                    <td>{{ item.username }}</td>
                    <td>{{ item.email }}</td>
                    <td>
                      <i
                        :class="{
                          'bi-check-circle text-success': item.is_admin,
                          'bi-x-circle text-danger': !item.is_admin,
                        }"
                      ></i>
                    </td>
                  </template>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <ErrorToast v-if="error" :message="error" @dismiss="error = null" />
    </div>
  </div>
</template>

<style scoped>
.badge {
  font-size: 0.85rem;
}
</style>
