<template>
  <div class="flex flex-col gap-2">
    <table class="abyssinica-sil-regular overflow-x-scroll">
        <thead>
            <tr>
                <th
                    v-for="field, fieldName in props.fields"
                    class="text-nowrap text-[12px] text-table-secondary text-left px-5 h-[40px]"
                    :data-centered="field.centerTitle"
                >
                    <span class="flex place-items-center h-full w-full gap-1 fill-text-secondary stroke-text-secondary">
                        {{ field.title }}

                        <!-- sort controls later -->
                        <span
                            v-if="!field.disableSorting || field.filterMode"
                            class="ml-auto mr-0 flex gap-1"
                        >
                            <BsSortDown
                                v-if="!field.disableSorting && sorting[ fieldName ] === 'asc'"
                                size="16"
                                class="fill-inherit"
                                @click="sorting[ fieldName ] = 'desc'"
                            />
                            <BsSortUp
                                v-else-if="!field.disableSorting && sorting[ fieldName ] === 'desc'"
                                size="16"
                                class="fill-inherit"
                                @click="delete sorting[ fieldName ]"
                            />
                            <BsSortDown
                                v-else-if="!field.disableSorting"
                                size="16"
                                class="fill-inherit unsorted"
                                @click="sorting[ fieldName ] = 'asc'"
                            />

                            <div
                                class="filter-container relative flex"
                                v-if="field.filterMode"
                            >
                                <TbFilter
                                    size="16"
                                    class="filter-inactive stroke-inherit"
                                />

                                <TbFilterFilled
                                    size="16"
                                    class="fill-inherit filter-active"
                                />

                                <!-- TbFilterCheck if filter applied -->

                                <input
                                    class="absolute w-fit inset-0 opacity-0 cursor-pointer"
                                    type="checkbox"
                                ></input>

                                <!-- todo: dynamic unique items -->
                                <InputUniqueOptions
                                    class="absolute top-full right-0 my-1 filter-input"
                                    v-if="field.filterMode === 'unique'"
                                    :options="field.filterInputOptions || [ 'none' ]"
                                    @select="( opts ) => {
                                        if ( opts.length === 0 ) delete filters[ fieldName ];
                                        else filters[ fieldName ] = opts;
                                    }"
                                />
                            </div>

                        </span>
                    </span>
                </th>
            </tr>
        </thead>
        <tbody>
            <!-- one row for each perPage count -->
            <tr
                v-for="entryIndex in ( Math.min( props.entries.length, pageData.isLastPage ? pageData.entriesLastPage : perPage ) )"
                class="text-center"
            >
                <td
                    v-for="field, _name in props.fields"
                    class="px-6 w-fit py-2"
                    :data-centered="field.centerEntries"
                    :data-fit-text="field.fitContent"
                >
                    <div>
                        <!-- should be able to be 100% sure entry exists, can let typescript know we know so -->
                        <!-- fix: Spread types may only be created from object types.ts-plugin(2698) -->
                        <component
                            v-if="getEntry( entryIndex - 1 ) && getEntry( entryIndex - 1 )[ _name ]"
                            :is="field.component"
                            v-bind="getEntry( entryIndex - 1 )[ _name ]"
                            class="text-table-normal text-sm"
                        />
                    </div>
                </td>
            </tr>
        </tbody>
    </table>

    <div
        v-if="props.entries.length === 0"
        class="py-2.5 w-full"
    >
        <p
            class="mx-auto w-fit"
        >Pole andmeid mida naidata</p>
    </div>

    <div
        class="flex gap-2 pagination min-h-fit"
    >
        <Button
            :disabled="currentPage === 0"
            class="disabled:bg-neutral-200 disabled:border-transparent transition-colors disabled:fill-text-disabled"
            @click="( ) => {
                currentPage -= 1
            }"
        >
            <BiChevronLeft size="20" class="fill-inherit" />
        </Button>

        <Button
            class="w-[40px] [&[data-selected=true]]:border-primary-normal [&[data-selected=true]]:text-primary-normal transition-colors"
            v-for="pageIdx in pageData.pageCountTotal"
            :data-selected="currentPage === ( pageIdx - 1 )"
            @click=" ( ) => {
                currentPage = pageIdx - 1;
            }"
        >
            {{ pageIdx }}
        </Button>

        <Button
            :disabled="currentPage === pageData.pageCountTotal - 1"
            class="disabled:bg-neutral-200 disabled:border-transparent transition-colors disabled:fill-text-disabled"
            @click="( ) => {
                currentPage += 1
            }"
        >
            <BiChevronRight size="20" class="fill-inherit" />
        </Button>

        <Select
            class="ml-2"
            :options="pageAmountSelection"
            :default-selected="pageAmountSelection.indexOf( perPage )"
            @change="perPageAmount => {
                perPage = perPageAmount;
                // if new page amount sets the index out of bounds, clamp it to max pages
                currentPage = Math.min( currentPage, pageData.pageCountTotal - 1 );

            }"
        ></Select>
        <span class="abyssinica-sil-regular my-auto text-[14px]">/Page</span>
    </div>
  </div>
</template>

<script setup lang="ts">
/*
table has to be passed
    fields: fields to show at the top, each entry has to
            have a component/text based on field name/title

    entries:
            list of maps for each row, each entry should have
            mappings for field title/name->PropType
    
    filtering & sorting are only available if corresponding function exists in field
*/
import { computed, ref, watch } from 'vue';
import type { FieldsMap, RowEntry } from '../FilterTable';
import Button from '../atoms/Button.vue';
import { BiChevronLeft, BiChevronRight } from 'vue-icons-plus/bi';
import { TbFilter, TbFilterFilled, TbFilterCheck } from 'vue-icons-plus/tb';
import { BsSortDown, BsSortUp } from 'vue-icons-plus/bs';
import Select from '../atoms/Select.vue';
import InputUniqueOptions from '../atoms/filter-table/InputUniqueOptions.vue';

const emit = defineEmits<{
    "perPageChange": [ number ],
    "pageChange": [ number ]
}>( );

// type passed from prop
// so <FilterTable<EntryType> :fields="[...]" ... />
// https://stackoverflow.com/a/69733851
const props = withDefaults( defineProps<{
    fields: FieldsMap,
    // each row has an object for each field title/name
    entries: RowEntry< FieldsMap >[ ],
    perPage?: number,
    selectedPage?: number
}>( ), {
    perPage: 10,
    selectedPage: 0,
} );

const pageAmountSelection = [ 10, 20, 30, 40 ];
const currentPage = ref( props.selectedPage );
const perPage = ref( props.perPage );

type SortBy = "asc" | "desc";
type FieldSortMap = {
    [ K in keyof FieldsMap ]: SortBy
};

const sorting = ref< FieldSortMap >({ });


type FilterMap = {
    [ K in keyof FieldsMap ]: string[ ]
}

const filters = ref< FilterMap >({ })

// todo: add filtering
// ps: never a ref reactive to props, dont want a stateful component, we can use "effects" :)
// what do I call this? filtering and sorting would be done here
const mutatedEntries = computed( ( ) => {
    return props.entries.slice( ).filter( ( row, i ) => {
        // we look through each row on given filter
        // and check if any element of filters is inside of props
        
        // conjuction or disjunction
        // since theyre columns should be conjuction right
        // so if one fails, fail all
        // let failsAny = false;
        // nvm no need we can return early

        // this could be simplified a lot but I'm not going to do any more weird
        // type casts and risk obfuscating readability
        let filterEntries = Object.entries( filters.value );
        for ( const filterEntryIndex in filterEntries ) {
            // cant deconstruct in loop
            const filterEntry = filterEntries[ filterEntryIndex ];
            const [ fieldName, fieldFilters ] = filterEntry as never as [ string, string[ ] ];

            const fieldProps = props.fields[ fieldName ];
            if ( !fieldProps || !fieldFilters || !row[ fieldName ] ) continue;

            if ( fieldProps.filterFn ) {
                let passed = fieldProps.filterFn( fieldProps, fieldFilters );

                if ( !passed ) return false;
            } else {
                let matchedAny = false;
                // check if is substring or of substring for each prop
                for ( const prop of Object.values( row[ fieldName ] ) ) {
                    // inlay hints, tostring might not exist
                    const propAsStr = `${ prop }`;
                    if ( fieldFilters.some( f => propAsStr.includes( f ) || f.includes( propAsStr ) ) )
                        matchedAny = true;
                }

                if ( i == 1 ) console.log( fieldFilters, Object.entries( row[ fieldName ]  ) )

                if ( !matchedAny ) return false;
            }
        }

        return true;
    } ).sort( ( row1, row2 ) => {
        for ( const field in sorting.value ) {
            // sanity check
            if ( !props.fields[ field ] ) continue;

            // sort based on func or alphabetical
            let sortRes = 0;
            if ( props.fields[ field ].sortFn )
                sortRes = props.fields[ field ].sortFn( row1[ field ], row2[ field ] );
            else
                sortRes = Object.values( row1[ field ] ).join( " " ).localeCompare( Object.values( row2[ field ] ).join( " " ) )

            // same value, go to next sorted column
            if ( sortRes === 0 ) continue;
            return sorting.value[ field ] === "asc" ? sortRes : -sortRes;
        }
        return 0;
    } );
} );

// pagination effects
watch(
    ( ) => perPage.value,
    ( newPerPage ) => emit( "perPageChange", newPerPage ) );

watch(
    ( ) => currentPage.value,
    ( newPage ) => emit( "pageChange", newPage )
)

const pageData = computed<{
    pageBaseCount: number,
    pageCountTotal: number
    entriesLastPage: number,

    hasFullLastPage: boolean,
    isLastPage: boolean
}>( ( ) => {
    // todo: should we use props entries or queried entries?
    const entries = mutatedEntries.value;

    // get page count, eg 40 items, 10 per page -> 4.0 (-> 4.0)
    // 40 items, 30 per page -> 1.33... -> 1.0
    const pageBaseCount = Math.floor( entries.length / perPage.value );

    // 40 items, if pagecount base (above) is eg 4.0 (10 per page), last page is full (4.0 * 10 = 40 -> 40 - 40 = 0)
    // 40 items, pagecount 1.33... (30 per page), last page is 1.0 * 30 = 30 -> 40 - 30 = 10, last page is not full 
    const hasFullLastPage = ( entries.length - pageBaseCount * perPage.value ) === 0;

    // page diff === 0 -> last page has pageCountBase items (aka max there can be on one page)
    // 40 items, page diff !== 0, 40 - 1.0 * 30 = 10 items on last page 
    const entriesLastPage = hasFullLastPage ? perPage.value : entries.length - pageBaseCount* perPage.value;

    // total page count, if we dont have a full last page, just return base page count (since no remainder items)
    // else, add 1 page,, since there's a page witth <basecount items
    let pageCountTotal = pageBaseCount + ( hasFullLastPage ? 0 : 1 );
    // in case we have no entries, clamp to a minimum 0f 1 page
    pageCountTotal = Math.max( 1, pageCountTotal );


    const isLastPage = pageCountTotal - 1 === currentPage.value;

    return {
        pageBaseCount,
        pageCountTotal,
        entriesLastPage,
        hasFullLastPage,
        isLastPage
    }
} );

// clamp page on init, could get to a bug where a cat is on the last page, gets removed and page handler gets "confused"
currentPage.value = Math.max( 0, Math.min( pageData.value.pageCountTotal - 1, currentPage.value ) );
// also sanity check perpage
perPage.value = pageAmountSelection.includes( perPage.value ) ? perPage.value : pageAmountSelection[ 0 ]!;

const getEntry = ( index: number ): RowEntry< FieldsMap > => {
    return mutatedEntries.value[ currentPage.value * perPage.value + index ] as RowEntry< FieldsMap >;
}

</script>

<style lang="css" scoped>
th:has( + th ),
td:has( + td ) {
    border-right: 1px solid var( --table-border );
}
tr:has( + tr ) {
    border-bottom: 1px solid var( --table-border );
}

td {
    vertical-align: middle;
}

td > div {
    display: flex;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 75ch;
    max-height: 6ch;
}

tr:nth-child( 2n ) {
    background: #f4f4f5;
}

td[data-centered=true] {
    text-align: center;

    & > div {
        justify-content: center;
    }
}

th[data-centered=true] span {
    margin: auto auto;
    width: fit-content;
}

td[data-fit-text=true] {
    min-width: fit-content;

    & * {
        text-wrap: nowrap;
    }
}

/* clip out the arrow from sort icon, since bs icon kit doesnt have an non-sorted
    might want to change icons later, they dont looks so good :(
*/
.unsorted {
    --sort-arrow: 35%;

    mask-clip: border-box;
    mask-composite: add;
    mask-image: linear-gradient( to right, #fff0, #fff0 var( --sort-arrow ), #ffff 0% );
}

.filter-active {
    display: none;
}
.filter-inactive {
    display: block;
}

.filter-container:has( input:checked ) {
    & .filter-input  {
        display: flex;
    }

    & .filter-active {
        display: block;
    }

    & .filter-inactive {
        display: none;
    }
}

.filter-input {
    display: none;
    border: 1px solid theme( "colors.text.disabled" );
    background: theme( "colors.main-bg" );
}
</style>
