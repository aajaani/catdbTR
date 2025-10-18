<template>
  <div
    class="flex flex-row bg-neutral-white min-h-10 border-neutral-400"
  >
  <!-- container for each entry as radio is invisible and takes all space -->
    <div
        v-for="( item, key ) in props.items"
        class="relative item-container flex flex-1 justify-center items-center border-t-[1px] border-b-[1px] border-neutral-400 border-solid"
        @click="( ) => {
            // items passed as string
            if ( typeof item === 'string' ) {
                emit( 'change', item );
                selected = item;
            } else {
                // items passed as individual components
                selected = ( key as string );
            }
        }"
    >
        <span
            v-if="typeof item === 'string'"
        >{{ item }}</span>

        <component
            v-else
            :is="( item as ItemAsComponent ).component"
            v-bind="( item as ItemAsComponent ).props"
        ></component>

        <input
            class="absolute inset-0 opacity-0 cursor-pointer"
            type="radio"
            :value="typeof item === 'string' ? item : key"
            :name="groupName"
            :defaultChecked="selected === ( typeof item === 'string' ? item : key )"
        ></input>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { Component } from 'vue';
import type { ComponentProps } from 'vue-component-type-helpers';

interface ItemAsComponent {
    component: Component,
    props: ComponentProps< Component >
}

type ItemsAsComponents = { [ key: string ]: ItemAsComponent };
type PropItemsType = ItemsAsComponents | readonly string[ ];

const props = defineProps<{
    groupName: string,
    items: PropItemsType,
    defaultSelected?: string
}>( );

// todo: check if defaultSelected exists in items

const emit = defineEmits<{
    "change": [ string ]
}>( );

// aha, ?? is more specific that ?
// if we have defaultSelected from props, use that as selected
// if not, pick first from passed items
const selected = ref( props.defaultSelected ?? (
    // objects don't have length
    props.items.length
        ? ( props.items as string[ ] )[ 0 ]
        // no length => dealing with object, use first key of object
        : Object.keys( props.items )[ 0 ]  )
);
</script>

<style lang="css" scoped>
.item-container:has( + .item-container ) {
    border-right: 1px solid;
    border-color: inherit;
}

.item-container:first-child {
    @apply rounded-l-md;
    border-left: 1px solid;
    border-left-color: inherit;
}

.item-container:last-child {
    @apply rounded-r-md;
    border-right: 1px solid;
    border-right-color: inherit;
}

.item-container:has( input:checked ) {
    @apply bg-[color-mix(in_srgb,theme(colors.primary.normal)_70%,white)];
}
</style>