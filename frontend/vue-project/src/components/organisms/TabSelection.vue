<template>
  <div class="grid grid-rows-[1fr_auto]">
    <!-- top items aka selectable items go here -->
    <div class="tabs-header bg-[color-mix(in_srgb,theme(colors.neutral.white)_96%,black)] flex flex-row min-h-[40px] rounded-md">
        <button
            type="button"
            v-for="( item, idx ) in props.tabs"
            @click="selected = idx"
            :data-active="selected === idx"
        >{{  item  }}</button>
    </div>

    <!-- """page""" content here -->
    <!-- okay, would do it as <slot :name="props.tabs[selected]"> -->
    <!-- but then we lose state, using `display: none` we never unload the children => no state loss  -->
    <div
        v-for="( tabName, idx ) in props.tabs"
        :key="tabName"
        :data-name="tabName"
        :style="{ display: selected === idx ? 'block' : 'none' }"
        class="tabs-content border-l border-r border-b rounded-b-md border-neutral-400 border-solid"
    >
        <slot :name="tabName"></slot>
    </div>

    <!-- old implementation -->
    <!-- <div class="tabs-content border-l border-r border-b rounded-b-md border-neutral-400 border-solid" :data-name="props.tabs[ selected ]">
        <slot :name="props.tabs[ selected ]"></slot>        
    </div> -->

  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';


// might need refactoring if we need tab names with spaces
const props = defineProps<{
    tabs: string[ ]
}>( );

const selected = ref( 0 );
</script>

<style lang="css" scoped>
.tabs-header {
    & button {
        @apply border-b border-neutral-400;
        flex: 1;
    
        &[ data-active=true ] {
            @apply bg-neutral-white border-r border-l border-t border-b-transparent  rounded-t-md;
        }
    }
}

.tabs-content > [aria-hidden] {
    display: none;
}
</style>