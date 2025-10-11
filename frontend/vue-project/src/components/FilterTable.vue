<template>
  <div>
    <table>
        <thead>
            <tr>
                <th
                    v-for="field in props.fields"
                >
                    {{ field.title }}
                </th>
            </tr>
        </thead>
        <tbody>
            <!-- one row for each entry -->
            <tr
                v-for="entry in props.entries"
            >
                <td
                    v-for="field in props.fields"
                >
                    <component
                        v-if="entry[ field.name ?? field.title ]"
                        :is="field.component"
                        v-bind="entry[ field.name ?? field.title ]"
                    >
                        {{ entry[ field.name ?? field.title ]?.innerText }}
                    </component>
                </td>
            </tr>
        </tbody>
    </table>
  </div>
</template>

<script setup lang="ts" generic="PassedType">
/*
    table has to be passed
    fields: fields to show at the top, each entry has to
            have a component/text based on field name
    filtering:
            fields should be filterable aswell, maybe default
            to alphabetical and have a custom filter function aswell
    sorting:
            same as filtering, default to alphabetical ordering,
            possible to supply a custom filter function
*/

/*
    do we have a value calculation function for each field? which then gets passed as
    keyvalue props to the component theyre a part of if the component exists?
*/

import type { Component } from 'vue';

interface TableField< EntryProps > {
    // text shown in table
    title: string,
    // name we look for in entry table,
    // if name doesn't exist, fall back
    // to title 
    name?: string,
    // component of table entry, table entry passes props to this component
    // to render it with
    component: Component< EntryProps > | keyof HTMLElementTagNameMap,
    // default sortFn to alphabetic
    sortFn?: ( props1: EntryProps, props2: EntryProps ) => number;
}

// type passed from prop
// so <FilterTable<EntryType> :fields="[...]" ... />
const props = defineProps<{
    fields: TableField< PassedType >[ ],
    // each row has an object for each field title/name
    // todo: stricter type for entry's type
    entries: { [ name: string ]: PassedType }[ ]
}>( );
</script>

<style lang="css" scoped>

</style>
