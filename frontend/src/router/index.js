import { createRouter, createWebHistory } from "vue-router";
import MainLogin from "@/pages/MainLogin.vue";
import RegisterPage from "@/pages/RegisterPage.vue";
import AdminDashboard from "@/pages/AdminDashboard.vue";
import UserDashboard from "@/pages/User/UserDashboard.vue";
import History from "@/pages/User/HistoryPage.vue";
import LotDetails from "@/pages/User/LotDetails.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", component: MainLogin },
  { path: "/register", component: RegisterPage },
  { path: "/admin/dashboard", component: AdminDashboard },
  { path: "/user/dashboard", component: UserDashboard },
  { path: "/user/parking_history", component: History },
  {
    path: "/lot/:id",
    component: LotDetails,
    name: "lot-details",
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
