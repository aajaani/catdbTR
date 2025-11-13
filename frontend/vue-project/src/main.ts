import './assets/main.css'

import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router/index.js'
import PrimeVue from 'primevue/config';
import ToastService from "primevue/toastservice";
import { client } from './gen_types/client.gen.ts';

const app = createApp(App)

client.setConfig({
    credentials: "include",
    baseUrl: import.meta.env.API_BASE_URL ?? "http://localhost:8000/",
})

app.use( router )
   .use( PrimeVue )
   .use( ToastService )

app.mount('#app')
