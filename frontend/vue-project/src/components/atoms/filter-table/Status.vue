<template>
  <span class="flex flex-row items-center gap-2">
    <span class="w-3 h-3 min-h-3 min-w-3 rounded-full status-circle" :data-color="props.color">

    </span>
    <p
      v-if="props.label"
      class="text-table-normal"
    >{{ props.label }}</p>
  </span>
</template>

<script setup lang="ts">
const props = defineProps<{
  color: "green" | "yellow" | "red" | "black" | "gray",
  label?: string
}>( )
</script>

<style lang="css" scoped>
.status-circle[data-color="green"] {
  background-color: #56BA28;
}

.status-circle[data-color="yellow"] {
  background-color: #FEBC2F;
}

.status-circle[data-color="red"] {
  background-color: #FF5F57;
}

.status-circle[data-color="black"] {
  background-color: #404040;
}

.status-circle[data-color="gray"] {
  background-color: #8C8C8C;
}
</style>