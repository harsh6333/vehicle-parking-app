import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: null,
    username: "",
    isAdmin: false,
  }),
  actions: {
    login({ token, username, is_admin }) {
      this.token = token;
      this.username = username;
      this.isAdmin = is_admin;
    },
    logout() {
      this.token = null;
      this.username = "";
      this.isAdmin = false;
    },
  },
  persist: true,
});
