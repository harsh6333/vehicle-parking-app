<template>
  <div class="stat-card" :class="{ 'stat-card-loading': loading }">
    <div class="stat-content">
      <div class="stat-text">
        <div class="stat-title">{{ title }}</div>
        <div v-if="!loading" class="stat-value">{{ value }}</div>
        <div v-else class="stat-loading"></div>
      </div>
      <div class="stat-icon" :class="`bg-${color}`">
        <i :class="`bi ${icon}`"></i>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  value: {
    type: [Number, String],
    required: true,
  },
  icon: {
    type: String,
    required: true,
  },
  color: {
    type: String,
    default: "primary",
  },
  loading: {
    type: Boolean,
    default: false,
  },
});
</script>

<style scoped>
.stat-card {
  background: white;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.03);
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  height: 100%;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
}

.stat-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-text {
  flex: 1;
}

.stat-title {
  font-size: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #6c757d;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.stat-value {
  font-size: 0.8rem;
  font-weight: 700;
  color: #2c3e50;
  line-height: 1.2;
}

.stat-icon {
  width: 32px;
  height: 32px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1rem;
}

.stat-loading {
  width: 80%;
  height: 32px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: 6px;
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* Color variants */
.bg-primary {
  background-color: var(--bs-primary) !important;
}
.bg-success {
  background-color: var(--bs-success) !important;
}
.bg-info {
  background-color: var(--bs-info) !important;
}
</style>
