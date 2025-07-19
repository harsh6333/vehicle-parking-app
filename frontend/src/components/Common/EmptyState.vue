<template>
  <div class="empty-state text-center" :class="`empty-state-${size}`">
    <i
      class="bi"
      :class="icon"
      :style="{ fontSize: size === 'sm' ? '2rem' : '3rem' }"
    ></i>
    <h5 class="mt-3">{{ title }}</h5>
    <p class="text-muted mb-3">{{ description }}</p>
    <button v-if="actionText" class="btn btn-primary" @click="$emit('action')">
      {{ actionText }}
    </button>
  </div>
</template>

<script setup>
defineProps({
  icon: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
  actionText: {
    type: String,
    default: "",
  },
  size: {
    type: String,
    default: "md",
    validator: (value) => ["sm", "md", "lg"].includes(value),
  },
});

defineEmits(["action"]);
</script>

<style scoped>
.empty-state {
  padding: 2rem 0;
}

.empty-state-sm {
  padding: 1rem 0;
}

.empty-state i {
  color: var(--bs-gray-400);
}
</style>
