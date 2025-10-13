<template>
  <button
    class="px-2.5 py-auto h-[40px] border-neutral-400 border-[1px] rounded-[8px] flex gap-2 justify-center items-center"
  >
    <slot name="icon"></slot>
    <slot></slot>
  </button>
</template>

<script setup>
import { ref } from 'vue';

const feature = ref();
</script>

<style lang="css" scoped>

</style>
