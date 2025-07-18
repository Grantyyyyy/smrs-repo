import { createPinia } from 'pinia';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { useAuthStore } from './stores/auth';

import Aura from '@primeuix/themes/aura';
import Button from 'primevue/button';
import PrimeVue from 'primevue/config';
import ConfirmationService from 'primevue/confirmationservice';
import Dialog from 'primevue/dialog';
import ToastService from 'primevue/toastservice';

import '@/assets/styles.scss';

const app = createApp(App);
const pinia = createPinia();

// Register PrimeVue components globally
app.component('Dialog', Dialog);
app.component('Button', Button);

// Register API endpoints


app.use(router);
app.use(pinia);

app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            darkModeSelector: '.app-dark'
        }
    }
});
app.use(ToastService);
app.use(ConfirmationService);

const authStore = useAuthStore();
authStore.initializeAuth();

app.mount('#app');
