<template>
  <div class="unique p-1 rounded-lg flex flex-col bg-white min-w-44 gap-1">
    <div class="flex flex-row flex-wrap gap-1 empty:hidden max-h-32 overflow-y-scroll bg-gray-100 rounded-[4px] border-solid border-[1px] border-text-disabled p-1">
        <!-- have to loop over all props options, otherwise ugly inline checks -->
        <span
            v-for="selectableOption in selectedOptions"
            class="flex-1 py-1 px-2 rounded-sm hover:bg-gray-200 bg-gray-200 bg-opacity-70 text-center select-none cursor-pointer"
            @click="( ) => {
                // filter out pressed item index
                selected = selected.filter( idx => idx !== selectableOption.arrIdx );
                $emit(
                    'select',
                    // update selected values callback
                    selectableOptions
                      // only let selected options stay
                      .filter( (_, idx) => selected.includes( idx ) )
                      // then map selected options to string, based if options are strings or components
                      .map( opt => typeof opt.option === 'string' ? opt.option : opt.option.searchName ) );
            }"
        >
            <span
                v-if="typeof selectableOption.option === 'string'"
            >
                {{ selectableOption.option }}
            </span>
            <component
                v-else
                class="flex-1"
                :is="selectableOption.option.component"
                v-bind="selectableOption.option.props"
            ></component>
        </span>
    </div>
    
    <div class="w-full h-[1px] border-b-0.5 border-b-table-border hidden"></div>

    <input
        v-model="searchQuery"
        type="text"
        class="w-full px-2 py-1 bg-gray-100 rounded-[4px] border-solid border-[1px] border-text-disabled"
        placeholder="Otsi"
    >

    <div
        class="flex flex-col gap-1 max-h-32 overflow-y-scroll bg-gray-100 rounded-[4px] border-solid border-[1px] border-text-disabled p-1 select-none"
    >
        <span
            v-for="selectableFiltereredOption in selectableOptions.filter( selectableOpt => filteredOptions.includes( selectableOpt.arrIdx ) && !selected.includes( selectableOpt.arrIdx ) )"
            class="p-1 hover:bg-gray-200 rounded-sm"
            @click="( ) => {
                selected.push( selectableFiltereredOption.arrIdx );
                $emit(
                    'select',
                    // same as for selecting
                    selectableOptions.filter( ( _, idx ) => selected.includes( idx ) ).map( selectedOpt => typeof selectedOpt.option === 'string' ? selectedOpt.option : selectedOpt.option.searchName )
                );
            }"
        >
            <span
                v-if="typeof selectableFiltereredOption.option === 'string'"
            >
                {{ selectableFiltereredOption.option }}
            </span>
            <component
                v-else
                :is="selectableFiltereredOption.option.component"
                v-bind="selectableFiltereredOption.option.props"
            ></component>
        </span>

        <span
            v-if="filteredOptions.filter( ( _, idx ) => !selected.includes( idx ) ).length === 0"
            class="p-1 rounded-sm"
        >
            Otsingutulemusi pole
        </span>
    </div>
  </div>
</template>

<script setup lang="ts" generic="Component">
import {ref, computed, defineComponent, watch} from 'vue';
import type { filterInputOptionsType, filterInputOptionType } from "@/components/FilterTable.ts";

const emit = defineEmits<{
    "select": [ selectedOptions: string[ ] ]
}>( );

type OptionType = filterInputOptionType< Component >

const props = defineProps<{
  // can be asynchronous
  options: filterInputOptionsType< Component >,
  isLoading?: boolean
}>( );

type SelectableOption = {
  option: OptionType,
  // we need the array index for showing filtered results
  // why? we only store the index for filtered results
  arrIdx: number
}

const make_option_selectable = ( ( opt: OptionType, arrIdx: number ) => {
    if ( typeof opt === "string" ) return { option: opt, arrIdx }
    return { option: { ...opt }, arrIdx }
} );

// we want to wait for oprions once
const selectableOptions = ref< SelectableOption[ ] >([ ]);

if ( typeof props.options === "function" ) {
    props.options( ).then( res => {
      selectableOptions.value = res.map( make_option_selectable );
    })
} else {
    selectableOptions.value = props.options.map( make_option_selectable );
}

const searchQuery = ref( "" );

// todo: could set selected by index
const selected = ref< number[ ] >([ ]);

const selectedOptions = computed( ( ) => {
    return selectableOptions.value.filter( ( _, idx ) => selected.value.includes( idx ) );
});

const filteredOptions = computed( ( ) =>
    selectableOptions.value.filter(
        ( selectableOption ) => (
            typeof selectableOption.option === "string"
                      ? selectableOption.option
                      : selectableOption.option.searchName
        ).includes( searchQuery.value )
    ).map( opt => opt.arrIdx )
);
</script>

<style lang="css" scoped>

</style>