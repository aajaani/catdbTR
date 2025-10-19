<template>
  <input
    type="text"
    pattern="([0-9]{0})|([0-9]{15})"
    :maxlength="props.numbers"
    :data-numbers="filled"
    v-model="filled"
  ></input>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const props = withDefaults( defineProps<{
    numbers: number,
    default?: string
}>( ), {
    default: ""
} )

const filled = ref( props.default );
</script>

<style lang="css" scoped>
input:focus:invalid {
    border-color: #e16666;
}

input:focus:valid {
    border-color: #66e166;
}

input {
    outline: none;
}
</style>