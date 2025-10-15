<template>
  <div class="unique p-1 rounded-lg flex flex-col bg-white min-w-44 gap-1">
    <div class="flex flex-row flex-wrap gap-1 empty:hidden max-h-32 overflow-y-scroll bg-gray-100 rounded-[4px] border-solid border-[1px] border-text-disabled p-1">
        <!-- have to loop over all props options, otherwise ugly inline checks -->
        <span
            v-for="option in selectedOptions"
            class="flex-1 py-1 px-2 rounded-sm hover:bg-gray-200 bg-gray-200 bg-opacity-70 text-center select-none cursor-pointer"
            @click="( ) => {
                selected = selected.filter( opt => opt != getOptName( option ) );
                $emit( 'select', selected );
            }"
        >
            <span
                v-if="typeof option === 'string'"
            >
                {{ option }}
            </span>
            <component
                v-else
                class="flex-1"
                :is="option.component"
                v-bind="option.props"
            ></component>
        </span>
    </div>
    
    <div class="w-full h-[1px] border-b-0.5 border-b-table-border hidden"></div>

    <input
        v-model="searchQuery"
        type="text"
        class="w-full px-2 py-1 bg-gray-100 rounded-[4px] border-solid border-[1px] border-text-disabled"
        placeholder="Otsi"
    ></input>

    <div
        class="flex flex-col gap-1 max-h-32 overflow-y-scroll bg-gray-100 rounded-[4px] border-solid border-[1px] border-text-disabled p-1 select-none"
    >
        <span
            v-for="selectableFilterName in filteredOptions.filter( opt => !arrIncludesOpt( selected, opt ) )"
            class="p-1 hover:bg-gray-200 rounded-sm"
            @click="( ) => {
                selected.push( getOptName( selectableFilterName ) );
                $emit( 'select', selected );
            }"
        >
            <span
                v-if="typeof selectableFilterName === 'string'"
            >
                {{ selectableFilterName }}
            </span>
            <component
                v-else
                :is="selectableFilterName.component"
                v-bind="selectableFilterName.props"
            ></component>
        </span>

        <span
            v-if="filteredOptions.filter( opt => !arrIncludesOpt( selected, opt ) ).length === 0"
            class="p-1 rounded-sm"
        >
            Otsingutulemusi pole
        </span>
    </div>
  </div>
</template>

<script setup lang="ts" generic="Component">
import { ref, computed, VueElement } from 'vue';
import type { ComponentProps, } from "vue-component-type-helpers";
import TableStatus from "@/components/atoms/filter-table/Status.vue"

const emit = defineEmits<{
    "select": [ selectedOptions: string[ ] ]
}>( );

// im not going to think of a jank solution to filter by Component props
// component could have innerText or child items inside it & I don't think
// its possible to filter by that
interface OptionAsComponent {
    component: Component,
    props: ComponentProps< Component >,
    searchName: string
}

// would be telling typescript that we have a list of either string or custom type
// but should be fine if we handle everything in "middleware" functions
//
// current solutions allows each entry to have a different component (kinda like ImGUI)
// if in the future (iteration 4 aka cleanup) we figure we don't need different components
// for each entry, we can pass the component from table header 
type OptionType = string | OptionAsComponent; 

const props = defineProps<{
    options: OptionType[ ],
}>( );

const searchQuery = ref( "" );

// todo: could set selected by index
const selected = ref< string[ ] >([ ]);

const selectedOptions = computed( ( ) => {
    return props.options.filter( opt => arrIncludesOpt( selected.value, opt) )
});

const optionIncludes = ( opt: OptionType, substr : string ) => {
    if ( typeof opt === "string" ) return opt.includes( substr );
    return opt.searchName.includes( substr );
}

// could be fancy and pass method but for readability sake separate funcs
// would maybe be useful if we have more than 2 methods
const arrIncludesOpt = ( arr: string[ ], opt: OptionType ) => {
    if ( typeof opt === "string" ) return arr.includes( opt );
    return arr.some( o => o === opt.searchName );
}

const getOptName = ( opt: OptionType ) => typeof opt === "string" ? opt : opt.searchName;

const filteredOptions = computed( ( ) => props.options.filter( ( opt ) => optionIncludes( opt, searchQuery.value ) ) );


</script>

<style lang="css" scoped>

</style>