<template>
  <!-- todo: could make the container a separate component to reduce rewrites for each view with breadcrumbs and title -->
  <div class="flex flex-col bg-main-bg px-8 pt-4">
    <h1 class="abril-fatface-regular text-[46px]">Vabatahtlikud</h1>
    <BreadCrumbs />

    <FilterTable
        :fields="fields"
        :entries="entries"
        :per-page="tableQueryParams.perPage"
        :selected-page="tableQueryParams.page - 1"
        @page-change="( page ) => {
          tableQueryParams.page = page + 1;
        }"
        @per-page-change="( perPage ) => {
          tableQueryParams.perPage = perPage;
        }"
      />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import BreadCrumbs from '@/components/organisms/BreadCrumbs.vue';
import { defineTable, field } from "@/components/FilterTable.ts"
import FilterTable from "@/components/organisms/FilterTable.vue"
import TableText from "@/components/atoms/filter-table/Text.vue"
import TableStatus from "@/components/atoms/filter-table/Text.vue"
import Actions from '@/components/molecules/filter-table/Actions.vue';
import { useRouter } from "vue-router";

type ManagerActivityStatus = "active" | "inactive";

const router = useRouter( )

const getQueryParam = ( name: string, def: string ) => {
  const queryParam = router.currentRoute.value.query[ name ];
  if ( !queryParam ) return def;
  return queryParam.toString( );
}

const tableQueryParams = ref<{
  page: number,
  perPage: number
}>({
  page: parseInt( getQueryParam( "page", "1" ) ),
  perPage: parseInt( getQueryParam( "perPage", "10" ) ),
});

// router.replace({ name: router.currentRoute.value.name, query: { page } })
watch(
  ( ) => tableQueryParams.value,
  ( newParams ) => {
    router.replace({ name: router.currentRoute.value.name, query: { ...newParams } })
  },
  {
    deep: true
  }
);

// todo: stricter types
// right now we're not accounting for undefined
const status_to_color: { [ key: string ]: string } = {
  "active": "green",
  "inactive": "red"
}
const status_to_readable: { [ key: string ]: string } = {
  "active": "Aktiivne",
  "inactive": "Mitte Aktiivne"
}


const { fields, entries } = defineTable({
    "manager-id": field({
      title: "#",
      component: TableText,
      disableSorting: true,
      centerEntries: true,
      centerTitle: true
    }),
    "managaer-name": field({
      title: "Nimi",
      component: TableText,
    }),
    "manager-status": ({
      title: "Staatus",
      component: TableStatus,
      fitContent: true,
      filterMode: "unique",
      filterInputOptions: ( [ "active", "inactive" ] ).map( s => ({
        component: TableStatus,
          props: {
            color: status_to_color[ s ],
            label: status_to_readable[ s ]
          },
          searchName: status_to_readable[ s ]
      }))
    }),
    "manager-phone": field({
      title: "Telefoninumber",
      component: TableText,
      fitContent: true,      
    }),
    "manager-email": field({
      title: "E-Mail",
      component: TableText,
    }),
    "manager-role": field({
      title: "Ametikoht",
      component: TableText,
    }),
    "manager-actions": field({
      title: "",
      component: Actions,
      disableSorting: true
    })
  },
  [ ]
);
</script>

<style lang="css" scoped>

</style>