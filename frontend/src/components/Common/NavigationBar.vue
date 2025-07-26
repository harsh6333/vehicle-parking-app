<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm py-3">
    <div class="container-fluid">
      <!-- Brand -->
      <router-link
        class="navbar-brand fw-bold d-flex align-items-center"
        to="/"
      >
        <i class="bi bi-car-front me-2 fs-4"></i>
        <span class="fs-5">ParkSmart</span>
      </router-link>

      <!-- Toggler for mobile -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarContent"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Collapsible Content -->
      <div class="collapse navbar-collapse" id="navbarContent">
        <!-- Left Menu -->
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item" v-for="item in navigation" :key="item.link">
            <router-link class="nav-link" active-class="active" :to="item.link">
              <i v-if="item.icon" :class="`${item.icon} me-2`"></i>
              {{ item.title }}
            </router-link>
          </li>
        </ul>

        <!-- Right Menu -->
        <div class="d-flex align-items-center gap-3">
          <!-- User Dropdown -->
          <div class="dropdown">
            <button
              class="btn btn-outline-light dropdown-toggle d-flex align-items-center"
              type="button"
              id="userDropdown"
              data-bs-toggle="dropdown"
            >
              <span
                class="avatar rounded-circle bg-white text-primary fw-bold me-2 d-inline-flex justify-content-center align-items-center"
              >
                {{ userInitials.initials }}
              </span>
              <span class="fw-semibold">{{ userInitials.username }}</span>
            </button>
            <ul class="dropdown-menu dropdown-menu-end">
              <li>
                <router-link class="dropdown-item" to="/profile">
                  <i class="bi bi-person me-2"></i>Profile
                </router-link>
              </li>
              <li><hr class="dropdown-divider" /></li>
              <li>
                <button class="dropdown-item text-danger" @click="logout">
                  <i class="bi bi-box-arrow-right me-2"></i>Logout
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { onMounted, computed } from "vue";
import { useAuthStore } from "@/store/auth";
import { useRouter } from "vue-router";
defineProps({
  navigation: {
    type: Array,
    required: true,
    default: () => [],
    validator: (items) => {
      return items.every(
        (item) =>
          typeof item === "object" &&
          typeof item.title === "string" &&
          typeof item.link === "string"
      );
    },
  },
});
const auth = useAuthStore();
const router = useRouter();

const userInitials = computed(() => ({
  username: auth?.user?.username || "User",
  initials:
    auth?.user?.username
      ?.split(" ")
      .map((name) => name.charAt(0))
      .join("")
      .slice(0, 2)
      .toUpperCase() || "US",
}));

const logout = () => {
  auth.logout();
  router.push("/login");
};

onMounted(async () => {
  await auth.fetchUser();
});
</script>

<style scoped>
.avatar {
  width: 32px;
  height: 32px;
  font-size: 0.9rem;
}
.navbar-nav .nav-link {
  font-weight: 500;
}
.dropdown-toggle:focus {
  box-shadow: none !important;
}
</style>
