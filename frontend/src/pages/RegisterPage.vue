<template>
  <div class="container-fluid min-vh-100 d-flex p-0">
    <!-- Left: Registration Form -->
    <div
      class="col-lg-5 d-flex align-items-center justify-content-center bg-white"
    >
      <div class="p-4 p-md-5 w-100" style="max-width: 400px">
        <div class="mb-4 text-center">
          <h2 class="fw-bold text-success">Register</h2>
          <p class="text-muted">Create your parking account</p>
        </div>

        <!-- Fields -->
        <div class="mb-3">
          <label class="form-label">Username</label>
          <input
            v-model="username"
            type="text"
            class="form-control"
            placeholder="Enter username"
          />
        </div>

        <div class="mb-3">
          <label class="form-label">Email</label>
          <input
            v-model="email"
            type="email"
            class="form-control"
            placeholder="Enter email"
          />
        </div>

        <div class="mb-3">
          <label class="form-label">Password</label>
          <input
            v-model="password"
            type="password"
            class="form-control"
            placeholder="Enter password"
          />
        </div>

        <div class="mb-3">
          <label class="form-label">Address</label>
          <input
            v-model="address"
            type="text"
            class="form-control"
            placeholder="Enter address"
          />
        </div>

        <div class="mb-3">
          <label class="form-label">Pincode</label>
          <input
            v-model="pincode"
            type="text"
            class="form-control"
            placeholder="Enter pincode"
          />
        </div>

        <!-- Vehicle Inputs -->
        <div class="mb-3">
          <label class="form-label">Vehicle Details</label>
          <div v-for="(v, i) in vehicles" :key="i" class="mb-2">
            <input
              v-model="v.vehicle_number"
              type="text"
              class="form-control mb-1"
              placeholder="Vehicle Number (e.g. KA-01-AB-1234)"
            />
            <input
              v-model="v.vehicle_type"
              type="text"
              class="form-control mb-1"
              placeholder="Vehicle Type (Car, Bike)"
            />
            <input
              v-model="v.brand"
              type="text"
              class="form-control mb-1"
              placeholder="Brand (e.g. Honda)"
            />
            <input
              v-model="v.color"
              type="text"
              class="form-control"
              placeholder="Color (e.g. Red)"
            />
            <hr />
          </div>
        </div>

        <!-- Submit -->
        <button @click="handleRegister" class="btn btn-success w-100 mb-3">
          Register
        </button>

        <!-- Alerts -->
        <div v-if="error" class="alert alert-danger text-center py-2">
          {{ error }}
        </div>
        <div v-if="success" class="alert alert-success text-center py-2">
          {{ success }}
        </div>

        <!-- Login -->
        <div class="text-center mt-3">
          <small>
            Already have an account?
            <router-link to="/login" class="fw-semibold text-decoration-none"
              >Login here</router-link
            >
          </small>
        </div>
      </div>
    </div>

    <!-- Right Image -->
    <div
      class="col-lg-7 d-none d-lg-flex align-items-center justify-content-center bg-light"
    >
      <img
        src="@/assets/heroImage.png"
        alt="Register Illustration"
        class="img-fluid p-5"
        style="max-height: 80%"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const username = ref("");
const email = ref("");
const password = ref("");
const address = ref("");
const pincode = ref("");
const vehicles = ref([
  { vehicle_number: "", vehicle_type: "", brand: "", color: "" },
  // { vehicle_number: "", vehicle_type: "", brand: "", color: "" },
  // { vehicle_number: "", vehicle_type: "", brand: "", color: "" },
]);

const error = ref("");
const success = ref("");
const router = useRouter();

const handleRegister = async () => {
  error.value = "";
  success.value = "";

  const validVehicles = vehicles.value
    .filter((v) => v.vehicle_number && v.vehicle_number.trim() !== "")
    .map((v) => ({
      vehicle_number: v.vehicle_number.trim(),
      vehicle_type: v.vehicle_type.trim(),
      brand: v.brand.trim(),
      color: v.color.trim(),
    }));

  if (
    !username.value ||
    !email.value ||
    !password.value ||
    !address.value ||
    !pincode.value ||
    validVehicles.length === 0
  ) {
    error.value =
      "All fields including at least one valid vehicle are required.";
    return;
  }

  try {
    await axios.post("http://127.0.0.1:5000/api/auth/register", {
      username: username.value,
      email: email.value,
      password: password.value,
      address: address.value,
      pin_code: pincode.value,
      vehicles: validVehicles,
    });

    success.value = "Registration successful! Redirecting...";
    setTimeout(() => router.push("/login"), 1500);
  } catch (err) {
    error.value = err.response?.data?.msg || "Registration failed.";
  }
};
</script>

<style scoped>
body {
  background-color: #f7fafd;
}
</style>
