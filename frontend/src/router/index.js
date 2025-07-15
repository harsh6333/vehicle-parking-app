import { createRouter, createWebHistory } from "vue-router";
import MainLogin from "@/pages/MainLogin.vue";
import RegisterPage from "@/pages/RegisterPage.vue";
import AdminDashboard from "@/pages/AdminDashboard.vue";
import UserDashboard from "@/pages/UserDashboard.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", component: MainLogin },
  { path: "/register", component: RegisterPage },
  { path: "/admin/dashboard", component: AdminDashboard },
  { path: "/user/dashboard", component: UserDashboard },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
