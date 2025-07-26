import { createRouter, createWebHistory } from "vue-router";
import MainLogin from "@/pages/MainLogin.vue";
import RegisterPage from "@/pages/RegisterPage.vue";
import AdminDashboard from "@/pages/Admin/AdminDashboard.vue";
import UserDashboard from "@/pages/User/UserDashboard.vue";
import History from "@/pages/User/HistoryPage.vue";
import LotDetails from "@/pages/User/LotDetails.vue";
import AllParkingLots from "@/pages/Admin/AllParkingLots.vue";
import PlatformUsers from "@/pages/Admin/PlatformUsers.vue";
import StatisticsChart from "@/pages/User/StatisticsChart.vue";
import StatisticsValues from "@/pages/Admin/StatisticsValues.vue";
import AdminSearch from "@/pages/Admin/AdminSearch.vue";
import HomePage from "@/pages/HomePage.vue";
import ProfilePage from "@/pages/ProfilePage.vue";

const routes = [
  { path: "/", component: HomePage },
  { path: "/login", component: MainLogin },
  { path: "/register", component: RegisterPage },
  { path: "/admin/dashboard", component: AdminDashboard },
  { path: "/admin/all_lots", component: AllParkingLots },
  { path: "/admin/all_users", component: PlatformUsers },
  { path: "/admin/statistics", component: StatisticsValues },
  { path: "/user/dashboard", component: UserDashboard },
  { path: "/user/parking_history", component: History },
  { path: "/user/statistics", component: StatisticsChart },
  {
    path: "/admin/search",
    name: "AdminSearch",
    component: AdminSearch,
  },
  {
    path: "/lot/:id",
    component: LotDetails,
    name: "lot-details",
    props: true,
  },
  { path: "/profile", component: ProfilePage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
