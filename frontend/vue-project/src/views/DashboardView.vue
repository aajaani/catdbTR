<script setup lang="ts">
import api from '@/api_fetch';
import type { CatRead } from '@/gen_types/types.gen';
import { computed, onMounted, ref } from 'vue';
import VCalendar from 'v-calendar';
import 'v-calendar/style.css';
import { Pie } from 'vue-chartjs'
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  Title
} from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend, Title);

const cats = ref<CatRead[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const date = ref(new Date());

const attrs = ref([
  {
    key: 'event1',
    dot: true,
    dates: new Date(2025, 10, 10, 18),
    popover: {label: 'Kassi kiibistamine'}
  },
])

function addEvent() {
  const newEventDate = new Date(2025, 10, 15);
  attrs.value.push({
    key: `event-${attrs.value.length + 1}`,
    dot: true,
    dates: newEventDate,
    popover: { label: `Uus sündmus` }
  });
}

const status_to_color: { [key in CatRead["status"]]: string } = {
  ACTIVE: "#50192f",     
  FOSTER: "#401B01",     
  ADOPTED: "#979797",    
  ARCHIVED: "#212121",   
  MISSING: "#FFFFFF",    
  RESERVED: "#bdbdbd"    
}

const status_to_readable: { [key in CatRead["status"]]: string } = {
  ACTIVE: "Otsib kodu",
  FOSTER: "Ajutises kodus",
  ADOPTED: "Uues kodus",
  ARCHIVED: "Kiisudemaal",
  MISSING: "Kadunud",
  RESERVED: "Broneeritud"
}

//counts per status
const statusCounts = computed(() => {
  const m = new Map<string, number>()
  cats.value.forEach(c => {
    const s = (c.status ?? 'unknown').toString()
    m.set(s, (m.get(s) ?? 0) + 1)
  })
  return Array.from(m.entries()) // [ [status, count], ... ]
})

const data = computed(() => {
  const labels: string[] = []
  const backgroundColors: string[] = []
  const values: number[] = []

  statusCounts.value.forEach(([status, count]) => {
    const readable = status_to_readable[status as keyof typeof status_to_readable] ?? status
    const color = status_to_color[status as keyof typeof status_to_color] ?? '#cccccc'
    labels.push(readable)
    backgroundColors.push(color)
    values.push(count)
  })

  return {
    labels,
    datasets: [
      {
        backgroundColor: backgroundColors,
        data: values
      }
    ]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'right' as const ,
      labels: {
        font: {
          size: 16,
          family: "abril-fatface-regular",
        },
        color: '#000000'
      }
    },
  }
}

onMounted(async () => {
  loading.value = true
  error.value = null
  try {
    const res = await api.listCatsCatsGet()
    // handle generated SDK shape (adjust if different)
    cats.value = res?.data ?? res
  } catch (e) {
    error.value = 'Failed to load cats data.'
  }
})
</script>

<template>
  <div class="abril-fatface-regular text-[46px] greetings">
    <h1>ÜLEVAADE</h1>
      <div class="diagram" >
        <div class="pie-wrap" > 
          <Pie :data="data" :options="chartOptions" />
        </div>
        <h2>
          <span class="flex-word">Kasside</span>
          <span class="flex-word"> staatuse</span>
          <span class="flex-word"> ülevaade</span>
        </h2>
      </div>

      <div class="kalender">
        <div class="kalender-header">
          <h4>Minu Kalender</h4>
        </div>

        <div class="kalender-body">
          <p class="kalender-item">Timeline</p>
          <VDatePicker transparent borderless show-weeknumbers v-model="date" mode="date" :attributes="attrs"  class="kalender-item" />
          <button class="add-event" > 
            <span class="hover-text" @click="addEvent">LISA +</span>
          </button>
        </div>
      </div>
  </div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: static;
  padding: 50px;
  margin-top: 3%;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  position: static;
  text-align: center;
  background-color: #D9D9D9;
  box-shadow: gray 0px 4px 14px -3px;
  padding-top: 50px;
}

.greetings h2{
  font-size: 2.6rem;
  text-align: center;
}

.diagram{
  display: flex;
  justify-content: center;
  margin-top: 5%;
  margin-right: 30%;
  margin-left: -15px;
  border-radius: 50px;
  background-color: #A69898;
  box-shadow: gray 0px 4px 14px -1px;
}

.diagram h2 {
  padding: 10%;
  margin-right: 0%;
}

.flex-word {
  display:flex;
  text-align: center;
  margin-top: 0%;
}

.pie-wrap {
  width: 400px;
  height: 400px;
  position: relative;
  margin: auto;
}

.kalender{
  position: flex;
  align-items: center;
  background-color: #D9D9D9;
  padding: 16px;
  box-shadow: gray 0px 4px 14px -3px;
  margin-top: 5%;
  border-radius: 8px;
}

.kalender-header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  margin-bottom: 12px;
}

.kalender-header h4 {
  font-size: 2.6rem;
}

.kalender-body {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.kalender-item {
  flex: auto;
  padding: 12px;
  text-align: center;
  font-size: 1.2rem;
}

.add-event {
  flex: auto;
  padding: 12px;
  margin-top: 5%;
  text-align: center;
  font-size: 2.6rem;
  cursor: default;
}

.hover-text {
  cursor: pointer;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: center;
  }
}
</style>
