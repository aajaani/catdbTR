<script setup lang="ts">
</script>

<template>
  <div class="abril-fatface-regular text-[46px] greetings">
    <h1>ÜLEVAADE</h1>
      <div class="diagram" >
        <h2>diagram</h2>
        <li class="list">
          <ul>
            <li>Otsivad kodu</li>
            <li>Uues kodus</li>
            <li>Broneeritud</li>
          </ul>
        </li>
        <h2>Kasside Staatuse Ülevaade</h2>
      </div>

      <div class="kalender">
        <div class="kalender-header">
          <h4>Minu Kalender</h4>
        </div>

        <div class="kalender-body">
          <p class="kalender-item">Timeline</p>
          <p class="kalender-item">Kalender</p>
          <p class="kalender-item">Add event</p>
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
  margin-top: 10%;
  margin-right: 20%;
  margin-left: -15px;
  border-radius: 16px;
  background-color: #A69898;
  box-shadow: gray 0px 4px 14px -1px;
}

.diagram h2 {
  padding: 50px;
}

.list {
  font-size: 1.5rem;
  list-style-type: none;
  padding: 50px;
}

.kalender{
  position: relative;
  background-color: #D9D9D9;
  padding: 16px;
  box-shadow: gray 0px 4px 14px -3px;
  margin-top: 10%;
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
@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: center;
  }
}
</style>
