import apiClient from '@/service/apiServices';
import tokenService from '@/service/tokenServices';
import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false,
    loading: false,
  }),

  getters: {
    userRole: (state) => state.user?.user_type || null,
    isStudent: (state) => state.user?.is_student || false,
    isInstructor: (state) => state.user?.is_instructor || false,
    isDSA: (state) => state.user?.is_dsa || false,
    isAdmin: (state) => state.user?.is_superuser || false,
  },

  actions: {
    async login(credentials) {
      this.loading = true;
      try {
        const response = await apiClient.post('token/', credentials);
        const { access, refresh, user} = response.data;
        
        this.user = user;
        this.isAuthenticated = true;
        
        return { success: true };
      } catch (error) {
        this.error = error.response?.data?.error || 'Login failed';

        if (error.response?.status === 401) {
          return { 
            success: false, 
            error: 'Your account is pending approval',
            errorType: 'pending' 
          };
        }

        return { success: false, error: 'Login failed' };
      } finally {
        this.loading = false;
      }
    },

    async logout() {
      try {
        const refreshToken = tokenService.getRefreshToken();
        if (refreshToken) {
          await apiClient.post('logout/', { refresh: refreshToken });
        }
      } catch (error) {
        console.error('Logout error:', error);
      } finally {
        tokenService.clearTokens();
        this.user = null;
        this.isAuthenticated = false;
        this.error = null;
      }
    },

    async initializeAuth() {
      const token = tokenService.getAccessToken();
      if (token && !tokenService.isTokenExpired(token)) {
        this.isAuthenticated = true;

        try {
          const response = await apiClient.get('me/');
          this.user = response.data;

          await this.FetchUserProfile();
        }catch (error) {
            console.error('Failed to fetch user profile:', error);
            tokenService.clearTokens();
            this.isAuthenticated = false;
        }
      } else {
        tokenService.clearTokens();
      }
    },

    async FetchUserProfile() {
      try {
        const response = await apiClient.get('me/');
        this.user = response.data;
      } catch (error) {
        console.error('Failed to fetch user profile:', error);
      }
    },

    clearError() {
      this.error = null;
    },
  },
});