<template>
    <div class="flex flex-row w-full">
        <input
            v-if="!!props.fallback"
            class="w-0 h-0 absolute"
            :name="groupName"
            :value="fallback"
            ref="fallback"
            v-model="model"
        ></input>

        <div
            class="flex flex-row w-full bg-neutral-white min-h-10 border-neutral-400"
        >

        <!-- container for each entry as radio is invisible and takes all space -->
            <div
                v-for="( item, key ) in props.items"
                class="relative item-container flex flex-1 justify-center items-center border-t-[1px] border-b-[1px] border-neutral-400 border-solid"
            >
                <span
                    v-if="typeof item === 'string'"
                >{{ item }}</span>

                <component
                    :is="( item as ItemAsComponent ).component"
                    v-bind="( item as ItemAsComponent ).props"
                ></component>

                <input
                    class="absolute inset-0 opacity-0 cursor-pointer"
                    type="radio"
                    :value="getRadioValue( item as ( string | ItemAsComponent ), key as string)"
                    :name="groupName"
                    v-model="model"
                    :title="props.fallback && `Paremklikk, et tuhistada sisestus`"
                    @click.right.prevent="( ) => {
                        if ( !props.fallback ) return;
                        let selected = props.fallback;
                        if ( fallbackInput ) fallbackInput.click( );
                        $emit( 'update:modelValue', selected );
                    }"
                ></input>
            </div>
        </div>
  </div>
</template>

<script setup lang="ts">
import { useTemplateRef } from 'vue';
import type { Component } from 'vue';
import type { ComponentProps } from 'vue-component-type-helpers';

type ItemAsComponent = {
    component: Component,
    props: ComponentProps< Component >
};

type ItemsAsComponents = { [ key: string ]: ItemAsComponent | string };
type PropItemsType = ItemsAsComponents | readonly string[ ];

const fallbackInput = useTemplateRef< HTMLInputElement | null >( "fallback" );

const props = defineProps<{
    groupName: string,
    items: PropItemsType,
    fallback?: string
}>( );

// todo: check if default mdoel value exists in items

const model = defineModel({ required: true });

const getRadioValue = ( item: string | ItemAsComponent, key: string ) => {
    if ( Array.isArray( props.items ) )
        return item;

    // const items = ( props.items as ItemsAsComponents );
    // if ( typeof item === "string" )
    return key; // Object.entries( items ).find( ([ v ]) => v === item )?.[ 0 ]
}
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