<template>
  <span>
    {{  props.text  }}
  </span>
</template>

<script setup lang="ts">
const props = defineProps<{
    text: string
}>( );
</script>

<style lang="css" scoped>

</style>