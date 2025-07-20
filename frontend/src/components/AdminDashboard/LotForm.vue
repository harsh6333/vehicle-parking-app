<template>
  <form
    @submit.prevent="handleSubmit"
    class="lot-form needs-validation"
    novalidate
    ref="formElement"
  >
    <div class="row g-3">
      <div class="col-md-6">
        <label class="form-label">Location Name</label>
        <input
          v-model="form.prime_location_name"
          class="form-control"
          placeholder="e.g. Connaught Place"
          required
        />
        <div class="invalid-feedback">Please provide a location name</div>
      </div>

      <div class="col-md-6">
        <label class="form-label">Address</label>
        <input
          v-model="form.address"
          class="form-control"
          placeholder="Street, Area, City"
          required
        />
        <div class="invalid-feedback">Please provide an address</div>
      </div>

      <div class="col-md-4">
        <label class="form-label">PIN Code</label>
        <input
          v-model="form.pin_code"
          class="form-control"
          placeholder="e.g. 110001"
          required
          pattern="[0-9]{6}"
        />
        <div class="invalid-feedback">
          Please provide a valid 6-digit PIN code
        </div>
      </div>

      <div class="col-md-4">
        <label class="form-label">Price Per Hour (₹)</label>
        <div class="input-group">
          <span class="input-group-text">₹</span>
          <input
            v-model.number="form.price"
            type="number"
            min="0"
            step="5"
            class="form-control"
            placeholder="e.g. 50"
            required
          />
        </div>
        <div class="invalid-feedback">Please provide a valid price</div>
      </div>

      <div class="col-md-4">
        <label class="form-label">Number of Spots</label>
        <input
          v-model.number="form.number_of_spots"
          type="number"
          min="1"
          class="form-control"
          placeholder="e.g. 20"
          required
        />
        <div class="invalid-feedback">Please provide at least 1 spot</div>
      </div>

      <div class="col-12 mt-4">
        <button class="btn btn-primary w-100 py-2" type="submit">
          <i
            class="bi"
            :class="form.id ? 'bi-pencil-square' : 'bi-plus-lg'"
          ></i>
          {{ form.id ? "Update Parking Lot" : "Create Parking Lot" }}
        </button>
      </div>
    </div>
  </form>
</template>

<script setup>
import { reactive, watch, ref } from "vue";

const props = defineProps(["modelValue"]);
const emit = defineEmits(["submit"]);

const formElement = ref(null);
const form = reactive({ ...props.modelValue });

watch(
  () => props.modelValue,
  (val) => Object.assign(form, val)
);

const handleSubmit = () => {
  if (formElement.value.checkValidity()) {
    emit("submit", { ...form });
  }
  formElement.value.classList.add("was-validated");
};
</script>

<style scoped>
.lot-form {
  padding: 1rem 0;
}

.form-control,
.input-group-text {
  border-radius: 8px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

.form-control:focus {
  border-color: var(--bs-primary);
  box-shadow: 0 0 0 0.25rem rgba(var(--bs-primary-rgb), 0.1);
}

.form-label {
  font-weight: 500;
  color: #495057;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.input-group-text {
  background-color: #f8f9fa;
}

.btn-primary {
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.invalid-feedback {
  font-size: 0.75rem;
}

/* Bootstrap validation styles */
.was-validated .form-control:invalid,
.was-validated .form-control.is-invalid {
  border-color: #dc3545;
  padding-right: calc(1.5em + 0.75rem);
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12' width='12' height='12' fill='none' stroke='%23dc3545'%3e%3ccircle cx='6' cy='6' r='4.5'/%3e%3cpath stroke-linejoin='round' d='M5.8 3.6h.4L6 6.5z'/%3e%3ccircle cx='6' cy='8.2' r='.6' fill='%23dc3545' stroke='none'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right calc(0.375em + 0.1875rem) center;
  background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
}

.was-validated .form-control:invalid:focus,
.was-validated .form-control.is-invalid:focus {
  border-color: #dc3545;
  box-shadow: 0 0 0 0.25rem rgba(220, 53, 69, 0.25);
}
</style>
