import axios from "axios";

const API = "http://127.0.0.1:5000/api/user";

const axiosInstance = axios.create({
  baseURL: API,
  withCredentials: true,
});

export const getLots = (date = null) => {
  const selectedDate = date || new Date().toISOString().split("T")[0];
  return axiosInstance.get(`/lots?date=${selectedDate}`);
};

export const fetchSpots = (lotId, date) =>
  axiosInstance.get(`/lots/${lotId}/spots`, {
    params: { date },
  });
export const reserveSpot = (spotId, start_time, durationHours) => {
  console.log(start_time);
  return axiosInstance.post("/reserve", {
    spot_id: spotId,
    start_time: start_time,
    duration_hours: durationHours,
  });
};

export const occupySpot = (resId, reserved_at) =>
  axiosInstance.put(`${API}/occupy/${resId}`, {
    reserved_at: new Date(reserved_at).toISOString(),
  });
export const releaseSpot = (resId, reserved_at) =>
  axiosInstance.put(`${API}/release/${resId}`, {
    reserved_at: new Date(reserved_at).toISOString(),
  });

export const getHistory = () => axiosInstance.get(`${API}/history`);
export const fetchUserStats = () => axiosInstance.get(`${API}/stats`);

export const triggerCSVExport = () => {
  return axiosInstance.post(`${API}/export/csv`);
};
