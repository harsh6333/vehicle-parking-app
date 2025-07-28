<template>
  <div class="landing-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-md-6">
            <h1 class="hero-title">Find & Reserve Parking Spots Instantly</h1>
            <p class="hero-subtitle">
              Book premium parking spaces near you with just a few taps
            </p>
          </div>
          <div class="col-md-6">
            <img
              src="@/assets/heroImage.png"
              alt="Parking illustration"
              class="hero-image"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <div class="container">
        <h2 class="section-title text-center">Why Choose Us</h2>
        <div class="row">
          <div class="col-md-4 feature-card">
            <div class="feature-icon">
              <i class="bi bi-clock"></i>
            </div>
            <h3>Instant Booking</h3>
            <p>Reserve your spot in seconds with our easy-to-use platform</p>
          </div>
          <div class="col-md-4 feature-card">
            <div class="feature-icon">
              <i class="bi bi-cash-coin"></i>
            </div>
            <h3>Best Prices</h3>
            <p>Competitive hourly rates with no hidden fees</p>
          </div>
          <div class="col-md-4 feature-card">
            <div class="feature-icon">
              <i class="bi bi-shield-check"></i>
            </div>
            <h3>Secure Parking</h3>
            <p>Verified locations with 24/7 security monitoring</p>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works -->
    <section class="how-it-works">
      <div class="container">
        <h2 class="section-title text-center">How It Works</h2>
        <div class="steps">
          <div class="step">
            <div class="step-number">1</div>
            <h3>Find Parking</h3>
            <p>Search for available spots near your destination</p>
          </div>
          <div class="step">
            <div class="step-number">2</div>
            <h3>Book & Pay</h3>
            <p>Select your time slot and complete payment</p>
          </div>
          <div class="step">
            <div class="step-number">3</div>
            <h3>Park Stress-Free</h3>
            <p>Your spot is reserved and waiting for you</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials -->
    <section class="testimonials py-5 bg-light">
      <div class="container">
        <h2 class="section-title text-center mb-5">What Our Users Say</h2>
        <div class="row">
          <div
            class="col-md-4 mb-4"
            v-for="(testimonial, index) in testimonials"
            :key="index"
          >
            <div class="testimonial-card p-4 rounded shadow-sm bg-white h-100">
              <div class="rating mb-3 text-warning">
                <i
                  class="bi bi-star-fill"
                  v-for="n in testimonial.rating"
                  :key="n"
                ></i>
              </div>
              <p class="mb-3 fst-italic">"{{ testimonial.comment }}"</p>
              <div class="user d-flex align-items-center gap-2">
                <img
                  :src="testimonial.avatar"
                  alt="User"
                  class="user-avatar rounded-circle"
                  style="width: 40px; height: 40px; object-fit: cover"
                />
                <span class="user-name fw-bold">{{ testimonial.name }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action -->
    <section class="cta-section">
      <div class="container text-center">
        <h2>Ready to Park with Ease?</h2>
        <p>Start booking online today</p>
        <div class="cta-buttons">
          <router-link to="/register" class="btn btn-primary btn-lg"
            >Sign Up</router-link
          >
          <router-link to="/login" class="btn btn-outline-light btn-lg"
            >Log In</router-link
          >
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
const testimonials = [
  {
    name: "Sarah J.",
    comment: "Saved me so much time finding parking downtown!",
    avatar: require("@/assets/user1.jpg"),
    rating: 5,
  },
  {
    name: "Raj Patel",
    comment: "Simple, intuitive, and reliable. Great for daily commutes.",
    avatar: require("@/assets/user2.avif"),
    rating: 4,
  },
  {
    name: "Emily R.",
    comment: "I use it every weekend. Booking is instant!",
    avatar: require("@/assets/user3.avif"),
    rating: 5,
  },
];
</script>

<style scoped>
@import "@/styles/homepage.css";
</style>
