import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
  state: {
    isAuthenticated: false,
  },
  mutations: {
    SET_AUTH(state, status) {
      state.isAuthenticated = status;
    },
  },
  actions: {
    login({ commit }, credentials) {
      return axios.post('/api/login/', credentials).then(() => {
        commit('SET_AUTH', true);
      }).catch(() => {
        commit('SET_AUTH', false);
      });
    },
    register({ commit }, data) {
      return axios.post('/api/register/', data).then(() => {
        commit('SET_AUTH', false);  // No autenticamos al usuario automáticamente tras el registro.
      });
    },
    requestPasswordReset({ commit }, email) {
      return axios.post('/api/request-password/', { email });
    },
    setNewPassword({ commit }, data) {
      return axios.post(`/api/set-new-password/${data.uidb64}/${data.token}/`, {
        password: data.password,
        password2: data.password2,
      });
    },
    logout({ commit }) {
      return axios.post('/api/logout/').then(() => {
        commit('SET_AUTH', false);
      });
    },
  },
  getters: {
    isAuthenticated: (state) => state.isAuthenticated,
  },
});
