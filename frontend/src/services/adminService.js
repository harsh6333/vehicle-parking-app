import axios from "axios";

const API = "http://127.0.0.1:5000/api/admin";

const axiosInstance = axios.create({
  baseURL: API,
  withCredentials: true,
});

export const fetchLots = () => axiosInstance.get("/lots");
export const createLot = (data) => axiosInstance.post("/lots", data);
export const deleteLotById = (id) => axiosInstance.delete(`/lots/${id}`);
export const updateLot = (id, data) => axiosInstance.put(`/lots/${id}`, data);
export const fetchSpots = (lotId) => axiosInstance.get(`/lots/${lotId}/spots`);
export const fetchUsers = () => axiosInstance.get("/users");
