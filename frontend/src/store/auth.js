import { defineStore } from "pinia";
import axios from "axios";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    isAdmin: false,
    isAuthenticated: false,
  }),
  actions: {
    async fetchUser() {
      try {
        const res = await axios.get("http://127.0.0.1:5000/api/auth/me", {
          withCredentials: true,
        });
        this.user = res.data;
        this.isAdmin = res.data.is_admin;
        this.isAuthenticated = true;
      } catch {
        this.logout();
      }
    },
    logout() {
      this.user = null;
      this.isAdmin = false;
      this.isAuthenticated = false;
    },
  },
});
