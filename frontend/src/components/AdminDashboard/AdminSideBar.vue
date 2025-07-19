<template>
  <aside class="admin-sidebar bg-dark text-white">
    <div class="d-flex flex-column h-100">
      <div class="sidebar-header p-3 border-bottom border-secondary">
        <router-link
          to="/admin/dashboard"
          class="text-white text-decoration-none d-flex align-items-center gap-2"
        >
          <i class="bi bi-car-front-fill text-primary fs-4"></i>
          <span class="fs-5 fw-semibold">Parking Admin</span>
        </router-link>
      </div>

      <nav class="nav flex-column flex-grow-1 p-3">
        <router-link
          to="/admin/dashboard"
          class="nav-link text-white d-flex align-items-center gap-2 py-2"
          active-class="active"
        >
          <i class="bi bi-speedometer2"></i>
          <span>Dashboard</span>
        </router-link>

        <router-link
          to="/users"
          class="nav-link text-white d-flex align-items-center gap-2 py-2"
          active-class="active"
        >
          <i class="bi bi-people"></i>
          <span>Users</span>
        </router-link>
      </nav>

      <div class="sidebar-footer p-3 border-top border-secondary">
        <div class="d-flex align-items-center gap-2">
          <div
            class="avatar bg-primary text-white rounded-circle d-flex align-items-center justify-content-center flex-shrink-0"
            style="width: 36px; height: 36px"
          >
            {{ userInitials.initials }}
          </div>
          <div class="text-truncate">
            <div class="fw-semibold text-truncate">
              {{ userInitials.username }}
            </div>
            <small class="text-muted">Administrator</small>
          </div>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  user: {
    type: Object,
    required: true,
  },
});

const userInitials = computed(() => {
  return {
    initials: props.user?.username?.substring(0, 2).toUpperCase() || "",
    username: props.user?.username,
  };
});
</script>

<style scoped>
.admin-sidebar {
  width: 280px;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 1000;
  transition: all 0.3s;
}

.nav-link {
  border-radius: 6px;
  transition: all 0.2s;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-link.active {
  background-color: rgba(13, 110, 253, 0.2);
  color: #0d6efd !important;
}

@media (max-width: 992px) {
  .admin-sidebar {
    width: 80px;
    overflow: hidden;
  }

  .sidebar-header span,
  .nav-link span {
    display: none;
  }

  .sidebar-footer > div > div {
    display: none;
  }

  .avatar {
    margin: 0 auto;
  }
}

@media (max-width: 768px) {
  .admin-sidebar {
    transform: translateX(-100%);
  }

  .admin-sidebar.show {
    transform: translateX(0);
  }
}
</style>
