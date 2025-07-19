<template>
  <div class="stat-card card bg-white border-0 shadow-sm h-100">
    <div class="card-body">
      <div class="d-flex justify-content-between">
        <div>
          <h6 class="text-muted mb-2">{{ title }}</h6>
          <template v-if="loading">
            <div class="placeholder-glow">
              <span class="placeholder col-4" style="height: 2rem"></span>
            </div>
          </template>
          <h3 v-else class="mb-0">{{ value }}</h3>
        </div>
        <div
          class="icon-circle"
          :class="`bg-${color}-bg-opacity-10 text-${color}`"
        >
          <i :class="`bi ${icon}`"></i>
        </div>
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
  border-radius: 10px;
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-3px);
}

.icon-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}
</style>
