<template>
  <div
    class="error-toast position-fixed bottom-0 end-0 p-3"
    style="z-index: 1100"
  >
    <div
      class="toast show"
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
    >
      <div class="toast-header bg-danger text-white">
        <strong class="me-auto">Error</strong>
        <button
          type="button"
          class="btn-close btn-close-white"
          @click="$emit('dismiss')"
          aria-label="Close"
        ></button>
      </div>
      <div class="toast-body">{{ message }}</div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  message: {
    type: String,
    required: true,
  },
});

defineEmits(["dismiss"]);
</script>
