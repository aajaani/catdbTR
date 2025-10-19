<script setup lang="ts">
import { RouterView } from 'vue-router'
import Navigation from "@/components/organisms/Navigation.vue"
</script>

<template>
  <!-- todo: no sidebar if not authed -->
  <!-- nav sidebar is always visible screens (todo: mobile view) -->
  <Navigation />

  <!-- main content changes based on route -->
  <RouterView />
</template>

<style scoped>
</style>
