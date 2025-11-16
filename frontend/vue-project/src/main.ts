import './assets/main.css'

import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router/index.ts'
import PrimeVue from 'primevue/config';
import ToastService from "primevue/toastservice";
import { client } from './gen_types/client.gen.ts';
import VCalendar from 'v-calendar'

const app = createApp(App)

client.setConfig({
    credentials: "include",
    baseUrl: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/",
})

app.use( router )
   .use( PrimeVue )
   .use( ToastService )
   .use( VCalendar, {})

app.mount('#app')
