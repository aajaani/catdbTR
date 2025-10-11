<template>
  <button
    class="px-2.5 py-2.5 border-neutral-400 border-[1px] rounded-[8px]"
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
