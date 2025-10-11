<template>
  <div>
    <table class="abyssinica-sil-regular overflow-x-scroll">
        <thead>
            <tr>
                <th
                    v-for="field, _name in props.fields"
                    class="text-nowrap text-[12px] text-table-secondary text-left px-5 h-[40px]"
                >
                    <span class="flex place-items-center h-full w-fit">
                        {{ field.title }}
                    </span>
                </th>
            </tr>
        </thead>
        <tbody>
            <!-- one row for each entry -->
            <tr
                v-for="entry in props.entries"
                class="text-center"
            >
                <td
                    v-for="field, _name in props.fields"
                    class="px-6 w-fit"
                    :data-centered="field.centerEntries"
                    :data-fit-text="field.fitContent"
                >
                    <div>
                        <component
                            v-if="entry[ _name ]"
                            :is="field.component"
                            v-bind="entry[ _name ]"
                            class="text-table-normal text-sm"
                        />
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
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
import type { FieldsMap, RowEntry } from '../FilterTable';

// type passed from prop
// so <FilterTable<EntryType> :fields="[...]" ... />
// https://stackoverflow.com/a/69733851
const props = withDefaults( defineProps<{
    fields: FieldsMap,
    // each row has an object for each field title/name
    entries: RowEntry< FieldsMap >[ ],
    perPage?: number
}>( ), {
    perPage: 20
} )
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
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 75ch;
    max-height: 6ch;
}

td[data-centered=true] {
    text-align: center;
}

td[data-fit-text=true] {
    min-width: fit-content;

    & * {
        text-wrap: nowrap;
    }
}
</style>
