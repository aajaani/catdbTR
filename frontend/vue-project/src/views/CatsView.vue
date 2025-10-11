<script setup lang="ts">

import BreadCrumbs from "@/components/BreadCrumbs.vue";
import FilterTable from "@/components/FilterTable.vue";
import type { Component } from 'vue';

interface TestInterface {
  innerText: string,
  "data-test": string
}
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

const fields: TableField< TestInterface >[ ] = [
  {
    title: "Visible Title",
    name: "field-name",
    component: "span",
  },
  {
    title: "Visible 2",
    name: "field-name2",
    component: "h1",
  },
  {
    title: "Visible 3",
    name: "field-name3",
    component: "p",
  }
];

const entries: { [ name: string ]: TestInterface }[ ] = [
  {
    "field-name": { innerText: "inner", "data-test": "1" },
    "field-name2": { innerText: "inner2", "data-test": "2" },
    "field-name3": { innerText: "inner3", "data-test": "3" },
  },
  {
    "field-name": { innerText: "inner", "data-test": "1" },
    "field-name2": { innerText: "inner2", "data-test": "2" },
    "field-name3": { innerText: "inner3", "data-test": "3" },
  },
  {
    "field-name": { innerText: "inner", "data-test": "1" },
    "field-name2": { innerText: "inner2", "data-test": "2" },
    "field-name3": { innerText: "inner3", "data-test": "3" },
  },
  {
    "field-name": { innerText: "inner", "data-test": "1" },
    "field-name2": { innerText: "inner2", "data-test": "2" },
    "field-name3": { innerText: "inner3", "data-test": "3" },
  },
]
</script>

<template>
  <div class="flex flex-col bg-main-bg px-8 pt-4">
    <!-- todo: kinda overlaps with collapse/back button -->
    <h1 class="abril-fatface-regular text-[46px]">Kassid</h1>
    <BreadCrumbs />

    <FilterTable
      :fields="fields"
      :entries="entries"
    />
  </div>
</template>

<style scoped>

</style>