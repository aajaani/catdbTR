<template>
  <div class="flex flex-row gap-2">
    <Button
        v-for="action in props.actions"
        :onclick="action.onClick"
    >
        <component
            :is="action.icon"
            size="20"
        />
        <span
            v-if="action.label"
        >{{ action.label }}</span>
    </Button>
  </div>
</template>

<script setup lang="ts">
import Button from "@/components/atoms/Button.vue"
import type { Component } from 'vue';

interface Action {
    icon: Component,
    label?: string,
    onClick: ( ) => void;
}

const props = defineProps<{
    actions: Action[ ]
}>( );
</script>

<style lang="css" scoped>

</style>