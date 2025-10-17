import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useUserStore } from "./useUserStore";

export const useAuthStore = defineStore("auth", () => {
  const accsesstoken = ref(localStorage.getItem("jwtTokenAccsess"));
  const refreshtoken = ref(localStorage.getItem("jwtTokenRefresh"));
  const userStore = useUserStore();
  function setAccsessToken(newToken) {
    accsesstoken.value = newToken;
    localStorage.setItem("jwtTokenAccsess", newToken);
  }
  function setRefreshToken(newToken) {
    refreshtoken.value = newToken;
    localStorage.setItem("jwtTokenRefresh", newToken);
  }
  function removeToken() {
    accsesstoken.value = null;
    refreshtoken.value = null;
    localStorage.removeItem("jwtTokenAccsess");
    localStorage.removeItem("jwtTokenRefresh");
  }
  let refreshInterval = null;

  async function refreshTokens() {
    if (!accsesstoken.value || !refreshtoken.value) {
      stopTokenRefresh();
      return false;
    }
    // try {
    //   if (!refreshtoken.value) {
    //     throw new Error("No refresh token available");
    //   }

    //   const response = await axios.post("/auth/auth/jwt/refresh/", {
    //     refresh: refreshtoken.value,
    //   });
    //   console.log(response, "resfers");
    //   if (!response.data.access) {
    //     throw new Error("Invalid token refresh response");
    //   }

    //   setAccsessToken(response.data.access);

    //   return true;
    // } catch (error) {
    //   console.error("Token refresh failed:", error);
    //   // При ошибке обновления выполняем выход
    //   logout();
    //   return false;
    // }

    return new Promise((resolve) => {
      setAccsessToken("accsess" + Date.now());
      setRefreshToken("refresh" + Date.now());
      resolve(true);
    });
  }
  function startTokenRefresh() {
    if (refreshInterval) {
      clearInterval(refreshInterval);
    }
    refreshTokens().then(() => {
      refreshInterval = setInterval(refreshTokens, 3000000);
    });
  }

  function stopTokenRefresh() {
    if (refreshInterval) {
      clearInterval(refreshInterval);
      refreshInterval = null;
    }
  }
  if (accsesstoken.value && refreshtoken.value) {
    startTokenRefresh();
  } else {
    stopTokenRefresh();
  }
  function logout() {
    removeToken();
    userStore.removeUser();
    roleStore.removeRole();
    stopTokenRefresh();
  }
  const getTokenAccsess = computed(() => accsesstoken.value);
  const getTokenRefresh = computed(() => refreshTokens.value);
  const isAuth = computed(() => !!accsesstoken.value && !!refreshtoken.value);
  async function login(url, formstate, mode) {
    // try {
    //   const response = await axios.post(url, formstate);
    //   if (!response?.data) {
    //     throw new Error("Сервер вернул пустой ответ");
    //   }
     

    //   console.log(response, "resp");
    //   if (mode === "login") {
    //     setAccsessToken(response.data.access);
    //     setRefreshToken(response.data.refresh);
    //   } else {
    //     console.log("fff");
    //     userStore.setUser(response.data);
    //     roleStore.setRole(response.data.is_root);
    //   }
    //   console.log(response.data.is_root, "root");

    //   startTokenRefresh();
    //   return true;
    // } catch (err) {
    //   console.error("Auth error:", err);
    //   if (err.response) {
    //     // Сервер вернул ошибку
    //     errorMessage =
    //       err.response.data?.non_field_errors?.[0] ||
    //       err.response.data?.detail ||
    //       err.response.data?.message ||
    //       err.response.data?.email[0] ||
    //       err.response.data?.nickname[0] ||
    //       JSON.stringify(err.response.data);
    //   } else if (err.request) {
    //     errorMessage = "Сервер не отвечает";
    //   } else {
    //     errorMessage = err.message;
    //   }
    //   return false;
    // } finally {
    // }

    return new Promise((resolve) => {
      setTimeout(() => {
        setAccsessToken("accsess");
        setRefreshToken("refresh");
        startTokenRefresh();
        resolve(true);
      }, 3000);
    });
  }
  return {
    logout,
    accsesstoken,
    refreshtoken,
    setAccsessToken,
    removeToken,
    getTokenAccsess,
    getTokenRefresh,
    isAuth,
    login,
    setRefreshToken,
  };
});