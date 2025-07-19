import { defineStore } from "pinia";
import {
  createLot,
  fetchLots,
  deleteLotById,
  fetchSpots,
  fetchUsers,
  updateLot,
} from "@/services/adminService";

export const useAdminStore = defineStore("admin", {
  state: () => ({
    lots: [],
    spots: [],
    users: [],
    loading: false,
    error: null,
    selectedLotId: null,
    selectedDate: new Date().toISOString().split("T")[0],
  }),

  getters: {
    totalSpots: (state) =>
      state.lots.reduce((sum, lot) => sum + lot.number_of_spots, 0),
    recentUsers: (state) => state.users.slice(0, 5),
    getLotById: (state) => (id) => state.lots.find((lot) => lot.id === id),
  },

  actions: {
    async fetchInitialData() {
      try {
        this.loading = true;
        await Promise.all([this.fetchLots(), this.fetchUsers()]);
      } catch (error) {
        this.setError(error);
      } finally {
        this.loading = false;
      }
    },

    async fetchLots() {
      try {
        this.loading = true;
        const res = await fetchLots();
        this.lots = res.data;
      } catch (error) {
        this.setError(error);
      } finally {
        this.loading = false;
      }
    },

    async fetchUsers() {
      try {
        this.loading = true;
        const res = await fetchUsers();
        this.users = res.data;
      } catch (error) {
        this.setError(error);
      } finally {
        this.loading = false;
      }
    },

    async fetchSpots(lotId, date) {
      try {
        this.loading = true;
        this.selectedLotId = lotId;
        this.selectedDate = date || this.selectedDate;

        const res = await fetchSpots(lotId, this.selectedDate);
        this.spots = res.data.spots;
      } catch (error) {
        this.setError(error);
      } finally {
        this.loading = false;
      }
    },

    async createLot(lotData) {
      try {
        this.loading = true;
        await createLot(lotData);
        await this.fetchLots();
      } catch (error) {
        this.setError(error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async updateLot(lotData) {
      try {
        this.loading = true;
        await updateLot(lotData.id, lotData);
        await this.fetchLots();
      } catch (error) {
        this.setError(error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async deleteLot(id) {
      try {
        this.loading = true;
        await deleteLotById(id);
        await this.fetchLots();

        if (this.selectedLotId === id) {
          this.spots = [];
          this.selectedLotId = null;
        }
      } catch (error) {
        this.setError(error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    setError(error) {
      this.error =
        error.response?.data?.message ||
        error.message ||
        "An unknown error occurred";
      console.error("AdminStore error:", error);

      // Auto-clear error after 5 seconds
      setTimeout(() => {
        this.error = null;
      }, 5000);
    },

    resetSelectedLot() {
      this.selectedLotId = null;
      this.spots = [];
    },
  },
});
