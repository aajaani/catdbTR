<template>
  <!-- todo: could make the container a separate component to reduce rewrites for each view with breadcrumbs and title -->
  <div class="flex flex-col bg-main-bg px-8 pt-4">
    <h1 class="abril-fatface-regular text-[46px]">Personal</h1>
    <BreadCrumbs />
  </div>
</template>

<script setup>
import BreadCrumbs from '@/components/organisms/BreadCrumbs.vue';
</script>

<style lang="css" scoped>

</style>