<template>
  <div class="col-md-4">
    <div class="card stat-card bg-white border-0 shadow-sm">
      <div class="card-body">
        <div class="d-flex justify-content-between">
          <div>
            <h6 class="text-muted mb-2">{{ title }}</h6>
            <h3 class="mb-0">{{ value }}</h3>
          </div>
          <div class="d-flex align-items-center justify-content-center">
            <div class="icon" :class="iconClass">
              <i :class="icon"></i>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps(["title", "value", "icon", "iconClass"]);
</script>

<style scoped>
.icon {
  height: 32px;
  width: 32px;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  justify-items: center;
}
</style>
