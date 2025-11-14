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
const showPopup = ref(false);

const CatName = ref('');
const time = ref('');
const Task = ref('');
const taskType = ref('');

const today = new Date()

const attrs = ref([
  // sample event
  {
    key: 'event1',
    dot: {
      
    },
    dates: new Date(2025, 10, 10, 18), //dates for some reason are 0-indexed months (10 = november)
    popover: {label: 'Kassi kiibistamine'},
  },
  {
    key: 'today',
    highlight: false,
    dates: today,
  }
])

function addEvent(catName: string, Date: Date, task: string, taskType: string) {
   // add a new event to the calendar and later persist info to db
  
  let typeColor= "#50192f"; //default color
  if (taskType === "VET_VISIT") {
    typeColor = "orange"; 
  } else if (taskType === "MEDICATION") {
    typeColor = "green"; 
  } else if (taskType === "PERSONAL") {
    typeColor = "blue"; 
  }
  
  const newEventDate = Date;
  attrs.value.push({
    key: `event-${attrs.value.length + 1}`,
    dot: {color: typeColor},
    dates: newEventDate,
    popover: { label: catName + ": " + task + taskType }
  });

  //reset input fields
  CatName.value = '';
  time.value = '';
  Task.value = '';
  taskType = '';
}

const status_to_color: { [key in CatRead["status"]]: string } = {
  //currently different from the CatsView.vue page, following the figma design as of now
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

//counts per status for pie chart
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
    const tasks = await api.listTasksTasksGet()
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

      <div v-if="showPopup" class="popup-overlay" @click.self="showPopup = false">
        <div class="popup-content">
          <div class="popup-inputs">
            <input type="text" v-model="CatName" placeholder="Kassi nimi" />
            <input type="date" v-model="time"/>
            <input type="text" v-model="Task" placeholder="Märkmed" />
              <div class="flex flex-col gap-2 p-4 w-full">
                <span class="text-base font-medium mb-1">Ülesande tüüp:</span>
                <div class="flex flex-col gap-2">
                  <label class="flex items-center gap-2 bg-[#F3F3F3] p-2 rounded-lg hover:bg-[#EAEAEA] transition text-sm">
                    <input type="radio" id="one" value="VET_VISIT" v-model="taskType" class="w-4 h-4 accent-[#50192f]" />
                    <span>Visiidi külastus</span>
                  </label>

                  <label class="flex items-center gap-2 bg-[#F3F3F3] p-2 rounded-lg hover:bg-[#EAEAEA] transition text-sm">
                    <input type="radio" id="two" value="MEDICATION" v-model="taskType" class="w-4 h-4 accent-[#50192f]" />
                    <span>Ravimi andmine</span>
                  </label>

                  <label class="flex items-center gap-2 bg-[#F3F3F3] p-2 rounded-lg hover:bg-[#EAEAEA] transition text-sm">
                    <input type="radio" id="three" value="PERSONAL" v-model="taskType" class="w-4 h-4 accent-[#50192f]" />
                    <span>Personaalne</span>
                  </label>
                </div>
              </div>
          </div>
          <button class="save-button" @click="addEvent(CatName, time, Task, taskType); showPopup=false">Salvesta</button>
        </div>
      </div>

      <div class="kalender">
        <div class="kalender-header">
          <h4>Minu Kalender</h4>
        </div>

        <div class="kalender-body">
          <p class="kalender-item">Timeline</p>
          <VDatePicker
            transparent
            borderless
            show-weeknumbers
            mode="date"
            :attributes="attrs"
            class="kalender-item"
            
          />

          <button class="add-event" > 
            <span class="hover-text" @click="showPopup=true">LISA +</span>
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

.popup-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
  z-index: 1000;;
}

.popup-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  background: #FFFFFF;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 0 20px rgba(0,0,0,0.3);
  width: 600px;
  max-width: 90vw;
}

.popup-inputs {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
  margin-bottom: 2rem;
}

.popup-inputs input {
  padding: 0.6rem;
  font-size: 1rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  width: 100%;
}

.save-button {
  background-color: #D9D9D9;
  border-radius: 16px;
  width: 100%;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: center;
  }
}
</style>
