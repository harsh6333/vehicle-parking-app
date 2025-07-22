import axios from "axios";

const API = "http://127.0.0.1:5000/api/admin";

const axiosInstance = axios.create({
  baseURL: API,
  withCredentials: true,
});
export const fetchDashboardData = () => axiosInstance.get("/dashboard");
export const fetchLots = () => axiosInstance.get("/lots");
export const createLot = (data) => axiosInstance.post("/lots", data);
export const deleteLotById = (id) => axiosInstance.delete(`/lots/${id}`);
export const updateLot = (id, data) => axiosInstance.put(`/lots/${id}`, data);
export const fetchSpots = (lotId, date) =>
  axiosInstance.get(`/lots/${lotId}/spots`, {
    params: { date },
  });

export const fetchUsers = () => axiosInstance.get("/users");
export const fetchSpotsForNow = (lotId) =>
  axiosInstance.get(`/lots/${lotId}/spots/current`);

export const fetchSpotHistory = (spotId) =>
  axiosInstance.get(`/spots/${spotId}/history`);
export const fetchAdminStats = () => axiosInstance.get(`${API}/stats`);
