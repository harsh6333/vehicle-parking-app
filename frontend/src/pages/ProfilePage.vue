<template>
  <div>
    <NavigationBar :navigation="navigationItems" />
    <div class="card mx-auto mt-4" style="max-width: 600px">
      <div class="card-header bg-primary text-white text-center">
        <h4 class="mb-0">My Profile</h4>
      </div>
      <div class="card-body">
        <div v-if="loading" class="text-center py-3">
          <div class="spinner-border text-primary"></div>
        </div>

        <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

        <form v-else @submit.prevent="handleSubmit">
          <div class="mb-3">
            <label class="form-label">Username</label>
            <input v-model="form.username" class="form-control" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Email</label>
            <input
              v-model="form.email"
              type="email"
              class="form-control"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Address</label>
            <input v-model="form.address" class="form-control" />
          </div>

          <div class="mb-3">
            <label class="form-label">Pin Code</label>
            <input v-model="form.pin_code" class="form-control" />
          </div>

          <div class="mb-3">
            <label v-if="form.vehicles.length > 0" class="form-label"
              >Vehicles</label
            >
            <div
              v-for="(vehicle, index) in form.vehicles"
              :key="index"
              class="input-group mb-2"
            >
              <input
                v-model="form.vehicles[index]"
                class="form-control"
                placeholder="Enter vehicle number"
              />
            </div>
          </div>

          <div class="mb-3">
            <label class="form-label">Role</label>
            <input
              :value="form.is_admin ? 'Admin' : 'User'"
              class="form-control"
              disabled
            />
          </div>

          <div class="d-flex justify-content-between">
            <button type="submit" class="btn btn-success">Update</button>
          </div>

          <div v-if="successMsg" class="alert alert-success mt-3">
            {{ successMsg }}
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { fetchProfile, updateProfile } from "@/services/commonService";
import NavigationBar from "@/components/Common/NavigationBar.vue";

const form = ref({
  username: "",
  email: "",
  address: "",
  pin_code: "",
  vehicles: [],
  is_admin: false,
});
const loading = ref(true);
const error = ref(null);
const successMsg = ref("");
const navigationItems = ref([]);

const fetchData = async () => {
  try {
    const res = await fetchProfile();
    Object.assign(form.value, {
      username: res.data.username,
      email: res.data.email,
      address: res.data.address || "",
      pin_code: res.data.pin_code || "",
      vehicles: res.data.vehicles?.map((v) => v.vehicle_number) || [],
      is_admin: res.data.is_admin,
    });

    navigationItems.value = form.value.is_admin
      ? [
          {
            title: "Dashboard",
            link: "/admin/dashboard",
            icon: "bi bi-speedometer2",
          },
          {
            title: "All Users",
            link: "/admin/all_users",
            icon: "bi bi-people",
          },
          {
            title: "All Lots",
            link: "/admin/all_lots",
            icon: "bi bi-building",
          },
          {
            title: "Summary",
            link: "/admin/statistics",
            icon: "bi bi-bar-chart",
          },
          { title: "Search", link: "/admin/search", icon: "bi-search" },
        ]
      : [
          {
            title: "Dashboard",
            link: "/user/dashboard",
            icon: "bi-speedometer2",
          },
          {
            title: "History",
            link: "/user/parking_history",
            icon: "bi-clock-history",
          },
          {
            title: "Statistics",
            link: "/user/statistics",
            icon: "bi-graph-up",
          },
        ];
  } catch (err) {
    error.value = err.response?.data?.msg || "Failed to load profile.";
  } finally {
    loading.value = false;
  }
};

const handleSubmit = async () => {
  try {
    const filteredVehicles = form.value.vehicles
      .map((v) => v.trim())
      .filter((v) => v !== "")
      .map((v) => ({ vehicle_number: v }));

    await updateProfile({
      username: form.value.username,
      email: form.value.email,
      address: form.value.address,
      pin_code: form.value.pin_code,
      vehicles: filteredVehicles,
    });

    successMsg.value = "Profile updated successfully!";
    setTimeout(() => (successMsg.value = ""), 3000);
  } catch (err) {
    error.value = err.response?.data?.msg || "Update failed.";
  }
};

onMounted(fetchData);
</script>
