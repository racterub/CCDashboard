import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import axios from "axios";

export default createStore({
  plugins: [createPersistedState()],
  state: {
    api: "https://ccdashboard.racterub.me/api",
    user: {
      name: "",
      loggedIn: false,
    },
    popMsg: {
      type: "",
      msg: "",
    },
  },
  mutations: {
    SETUSER(state, payload) {
      state.user.name = payload.name;
      state.user.loggedIn = payload.loggedIn;
    },
    SETPOPMSG(state, payload) {
      state.popMsg.type = payload.type;
      state.popMsg.msg = payload.msg;
    },
  },
  actions: {
    async sendLogout({ state }) {
      try {
        const res = await axios.get(`${state.api}/auth/logout`, {
          withCredentials: true,
        });
        if (res.data.status) {
          this.commit("SETUSER", { loggedIn: false, name: "" });
          this.commit("SETPOPMSG", { type: "success", msg: res.data.msg });
          return true;
        } else {
          return false;
        }
      } catch (error) {
        this.commit("SETPOPMSG", { type: "error", msg: "Unexpected error." });
        return false;
      }
    },
    async sendLogin({ state, commit }, payload) {
      try {
        const formData = new FormData();
        formData.append("username", payload.username);
        formData.append("password", payload.password);
        const res = await axios.post(`${state.api}/auth/login`, formData, {
          withCredentials: true,
        });
        if (res.data.status) {
          commit("SETUSER", { loggedIn: true, name: res.data.name });
          commit("SETPOPMSG", { type: "success", msg: res.data.msg });
          return true;
        } else {
          commit("SETPOPMSG", { type: "error", msg: res.data.msg });
          return false;
        }
      } catch (error) {
        commit("SETPOPMSG", { type: "error", msg: "Unexpected error." });
        return false;
      }
    },
    clearPopMsg({ commit }) {
      commit("SETPOPMSG", { type: "", msg: "" });
    },
    // async sendRegister({ state }, payload) {
    //   try {
    //     const formData = new FormData();
    //     formData.append("name", payload.name);
    //     formData.append("username", payload.username);
    //     formData.append("password", payload.password);
    //     formData.append("api_key", payload.api_key);
    //     formData.append("api_secret", payload.api_secret);
    //     const res = await axios.post(`${state.api}/auth/register`, formData);
    //     return res.data;
    //   } catch (error) {
    //     return error;
    //   }
    // },
    async checkAccount({ state }) {
      try {
        const res = await axios.get(
          `${state.api}/settings/checkAccountStatus`,
          {
            withCredentials: true,
          }
        );
        if (res.data.status) {
          return true;
        } else {
          return false;
        }
      } catch (error) {
        return false;
      }
    },
    async getSummary({ state, commit }, coin) {
      try {
        let endpoint = "";
        if (coin) {
          endpoint = `${state.api}/service/summary/${coin}`;
        } else {
          endpoint = `${state.api}/service/summary`;
        }
        const res = await axios.get(endpoint, {
          withCredentials: true,
        });
        if (res.data.status) {
          return res.data;
        } else {
          commit("SETPOPMSG", { type: "error", msg: res.data.msg });
          if (res.data.auth) {
            commit("SETUSER", { name: "", loggedIn: false });
          }
          return res.data;
        }
      } catch (error) {
        commit("SETPOPMSG", { type: "error", msg: "Unexpected error." });
        commit("SETUSER", { name: "", loggedIn: false });
        return { status: false };
      }
    },
    async getDashboard({ state, commit }) {
      try {
        const res = await axios.get(`${state.api}/service/dashboard`, {
          withCredentials: true,
        });
        if (res.data.status) {
          return res.data;
        } else {
          commit("SETPOPMSG", { type: "error", msg: res.data.msg });
          if (res.data.auth) {
            commit("SETUSER", { name: "", loggedIn: false });
          }
          return res.data;
        }
      } catch (error) {
        commit("SETPOPMSG", { type: "error", msg: "Unexpected error." });
        commit("SETUSER", { name: "", loggedIn: false });
        return { status: false };
      }
    },
    async getSpots({ state, commit }, payload) {
      try {
        const res = await axios.get(
          `${state.api}/service/spots/${payload.coin}`,
          {
            withCredentials: true,
          }
        );
        if (res.data.status) {
          return res.data;
        } else {
          commit("SETPOPMSG", { type: "error", msg: res.data.msg });
          if (res.data.auth) {
            commit("SETUSER", { name: "", loggedIn: false });
          }
          return res.data;
        }
      } catch (error) {
        commit("SETPOPMSG", { type: "error", msg: "Unexpected error." });
        commit("SETUSER", { name: "", loggedIn: false });
        return { status: false };
      }
    },
    async updatePassword({ state, commit }, payload) {
      try {
        const formData = new FormData();
        formData.append("oldPassword", payload.oldPassword);
        formData.append("newPassword", payload.newPassword);
        const res = await axios.post(
          `${state.api}/settings/updatePassword`,
          formData,
          {
            withCredentials: true,
          }
        );
        if (res.data.status) {
          commit("SETPOPMSG", { type: "success", msg: res.data.msg });
          return res.data;
        } else {
          commit("SETPOPMSG", { type: "error", msg: res.data.msg });
          if (res.data.auth) {
            commit("SETUSER", { name: "", loggedIn: false });
          }
          return res.data;
        }
      } catch (error) {
        commit("SETUSER", { name: "", loggedIn: false });
        commit("SETPOPMSG", { type: "error", msg: "Unexpected error." });
        return {
          auth: false,
          status: false,
        };
      }
    },
    // async updateBinance({ state }, payload) {
    //   try {
    //     const formData = new FormData();
    //     formData.append("newAPIKey", payload.newAPIKey);
    //     formData.append("newAPISecret", payload.newAPISecret);
    //     const res = await axios.post(
    //       `${state.api}/settings/updateBinance`,
    //       formData,
    //       {
    //         headers: {
    //           Authorization: `Bearer ${state.user.token}`,
    //         },
    //       }
    //     );
    //     return res.data;
    //   } catch (error) {
    //     return error;
    //   }
    // },
  },
  getters: {},
});
