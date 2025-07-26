<template>
  <div class="">
    <NavigationBar :navigation="navigationItems" />
    <div class="card mx-auto mt-4" style="max-width: 500px">
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
  role: "",
  created_at: "",
});
const loading = ref(true);
const error = ref(null);
const successMsg = ref("");
const navigationItems = ref([]);
const fetchData = async () => {
  try {
    const res = await fetchProfile();
    Object.assign(form.value, res.data);
    res.data?.is_admin
      ? (navigationItems.value = [
          {
            title: "Dashboard",
            link: "/admin/dashboard",
            icon: "bi bi-speedometer2",
          },
          {
            title: "All Users",
            link: "/admin/all_users",
            icon: "bi bi-clock-history",
          },
          {
            title: "All Lots",
            link: "/admin/all_lots",
            icon: "bi bi-clock-history",
          },
          {
            title: "Summary",
            link: "/admin/statistics",
            icon: "bi bi-clock-history",
          },
          {
            title: "Search",
            link: "/admin/search",
            icon: "bi-search",
          },
        ])
      : (navigationItems.value = [
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
        ]);
  } catch (err) {
    error.value = err.response?.data?.msg || "Failed to load profile.";
  } finally {
    loading.value = false;
  }
};

const handleSubmit = async () => {
  try {
    const res = await updateProfile({
      username: form.value.username,
      email: form.value.email,
    });
    Object.assign(form.value, res.data);
    successMsg.value = "Profile updated successfully!";
    setTimeout(() => (successMsg.value = ""), 3000);
  } catch (err) {
    error.value = err.response?.data?.msg || "Update failed.";
  }
};

onMounted(fetchData);
</script>
