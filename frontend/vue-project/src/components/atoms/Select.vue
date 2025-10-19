<template>
    <select
        class="border-neutral-400 border-[1px] rounded-lg px-3 gap-2 py-2 max-h-10 min-w-40 bg-white"
        @change="( e: Event ) => {
            const selectedIndex = ( e.target as HTMLSelectElement ).selectedIndex;
            if ( !( selectedIndex >= 0 && selectedIndex < props.options.length ) ) return;
            if ( !props.options[ selectedIndex ] ) return;

            $emit( 'change', props.options[ selectedIndex ] )
        }
        "
    >
        <option
            v-for="( opt, idx ) in props.options"
            :selected="idx === props.defaultSelected"
        >{{ opt }}</option>
    </select>
</template>

<script setup lang="ts" generic="OptionType">

const props = withDefaults( defineProps<{
    options: OptionType[ ]
    defaultSelected?: number
}>( ), {
    defaultSelected: 0
} );

const emit = defineEmits<{
    change: [ OptionType ]
}>( );
</script>