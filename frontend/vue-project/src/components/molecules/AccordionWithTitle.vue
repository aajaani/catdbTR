<template>
  <div class="grid grid-cols-1 accordion-container px-4 pt-4">
    <div
        class="flex gap-2 relative col-span-1 col-start-1 accordion-title items-center pb-4"
    >
        <bs-chevron-right
            size="20"
            class="icon fill-inherit"
        />
        <h1 class="text-2xl">{{ props.title }}</h1>
        
        <input
            type="checkbox"
            class="absolute inset-0 opacity-0"
            :checked="props.defaultOpened"
            :disabled="props.lock"
        ></input>
    </div>

    <div class="accordion-content">
        <slot></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { BsChevronRight } from 'vue-icons-plus/bs';

const props = defineProps<{
    title: string,
    lock?: boolean,
    defaultOpened?: boolean
}>( );
</script>

<style lang="css" scoped>
.accordion-container {
    grid-template-rows: auto 0fr;
    overflow: hidden;
    transition: grid-template-rows 200ms ease, padding-bottom 200ms ease;

    &:has( .accordion-title input:checked ) {
        grid-template-rows: auto 1fr;

        & .accordion-content {
            visibility: visible;
        }
    }

    & .accordion-content {
        min-height: 0;
        visibility: hidden;
        transition: visibility 200ms, margin-top 200ms;
    }
}

input[type=checkbox]:not( :disabled ) {
    cursor: pointer;
}

.icon {
    rotate: 0;
    transition: rotate 200ms ease;
}

.accordion-title:has( input:checked ) .icon {
    rotate: 90deg;
}

.accordion-title:has( input:disabled ) .icon {
    @apply fill-neutral-400;
}

/* omg i mightve thought of a way */
/* container bottom padding 1rem -> 0px */
/* title bottom padding 0 -> 1rem */
/* that way content is never visible when open */
.accordion-container:has( .accordion-title input:checked ) {
    padding-bottom: 1rem;
}
</style>