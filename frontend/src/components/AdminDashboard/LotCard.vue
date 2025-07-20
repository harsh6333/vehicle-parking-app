<template>
  <div class="lot-card">
    <div class="card-header">
      <div class="d-flex justify-content-between align-items-center">
        <h5 class="card-title">
          <i class="bi bi-geo-alt-fill"></i>
          {{ lot.prime_location_name }}
        </h5>
        <span class="badge"> {{ lot.total_spots }} spots </span>
      </div>
    </div>

    <div class="card-body">
      <ul class="lot-details">
        <li>
          <i class="bi bi-geo"></i>
          <span>{{ lot.address }}</span>
        </li>
        <li>
          <i class="bi bi-postcard"></i>
          <span>PIN: {{ lot.pin_code }}</span>
        </li>
        <li>
          <i class="bi bi-cash-coin"></i>
          <span>₹{{ lot.price }} / hour</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
defineProps(["lot"]);
</script>

<style scoped>
.lot-card {
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  background: white;
  transition: all 0.2s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.lot-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
}

.card-header {
  padding: 1.25rem 1.25rem 0.75rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.card-title {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--bs-primary);
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.badge {
  background: rgba(var(--bs-primary-rgb), 0.1);
  color: var(--bs-primary);
  padding: 0.35rem 0.65rem;
  border-radius: 6px;
  font-weight: 500;
  font-size: 0.8rem;
}

.card-body {
  padding: 1.25rem;
  flex-grow: 1;
}

.lot-details {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.lot-details li {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  font-size: 0.9rem;
  color: #5c6c75;
}

.lot-details i {
  color: var(--bs-primary);
  font-size: 1rem;
  margin-top: 0.1rem;
}

.card-footer {
  padding: 0.75rem 1.25rem;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.btn-action {
  width: 100%;
  background: rgba(var(--bs-primary-rgb), 0.05);
  color: var(--bs-primary);
  border-radius: 8px;
  padding: 0.5rem;
  font-weight: 500;
  border: none;
  transition: all 0.2s ease;
}

.btn-action:hover {
  background: rgba(var(--bs-primary-rgb), 0.1);
}
</style>
