import axios from "axios";

const API = "http://127.0.0.1:5000/api/auth/";

const axiosInstance = axios.create({
  baseURL: API,
  withCredentials: true,
});

export const fetchProfile = () => axiosInstance.get("/profile");
export const updateProfile = (data) => axiosInstance.put("/profile", data);
