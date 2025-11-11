<template>
  <!-- todo: could make the container a separate component to reduce rewrites for each view with breadcrumbs and title -->
  <div class="flex flex-col bg-main-bg px-8 pt-4">
    <h1 class="abril-fatface-regular text-[46px]">Vabatahtlikud</h1>
    <BreadCrumbs />

    <FilterTable
        :fields="tableDefinition.fields"
        :entries="tableDefinition.entries"
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
import { ref, watch, computed } from 'vue';
import BreadCrumbs from '@/components/organisms/BreadCrumbs.vue';
import { defineTable, field } from "@/components/FilterTable.ts"
import FilterTable from "@/components/organisms/FilterTable.vue"
import TableText from "@/components/atoms/filter-table/Text.vue"
import TableStatus from "@/components/atoms/filter-table/Status.vue"
import Actions from '@/components/molecules/filter-table/Actions.vue';
import { useRouter } from "vue-router";
import type { ManagerRead } from '@/gen_types/types.gen';
import { FcManager } from 'vue-icons-plus/fc';
import api from '@/api_fetch';



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
const status_to_color: Record<ManagerRead['status'], 'green' | 'red'> = {
  ACTIVE: 'green',
  INACTIVE: 'red',
};
const status_to_readable: Record<ManagerRead['status'], string> = {
  ACTIVE: 'Aktiivne',
  INACTIVE: 'Mitte aktiivne',
};

const role_to_readable: Record<ManagerRead['role'], string> = {
  MANAGER: 'Haldur',
  NOT_MANAGER: 'Pole haldur',
};

const managers = ref< ManagerRead[ ] >([ ]);

api.listManagersManagersGet().then( (res) => {
  console.log(res);
  managers.value = res.data
});


const fields = {
    "manager-id": field({
      title: "#",
      component: TableText,
      disableSorting: true,
      centerEntries: true,
      centerTitle: true
    }),
    "manager-name": field({
      title: "Nimi",
      component: TableText,
    }),
    "manager-status": field({
      title: "Staatus",
      component: TableStatus,
      fitContent: true,
      filterMode: "unique",
      filterInputOptions: (['ACTIVE', 'INACTIVE'] as ManagerRead['status'][]).map((s) => ({
        component: TableStatus,              // or TableStatus with { color, label }
        props: { 
          color: status_to_color[s],
          label: status_to_readable[s] 
        },
        searchName: status_to_readable[s]
      })),
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
    })
   /*  "manager-actions": field({
      title: "",
      component: Actions,
      disableSorting: true
    }) */


  };
  const tableDefinition = computed(() => defineTable(
    fields, 
    managers.value.map(( manager: ManagerRead) => ({
      "manager-id": {
        text:String(manager.id) 
      } as const,
      "manager-name": {
        text: manager.display_name
      } as const, 
      "manager-phone": {
        text: manager.phone ?? ""
      } as const,
      "manager-email": {
        text: manager.email 
      } as const,
      "manager-role": {
        text: role_to_readable[manager.role] 
      } as const,
      "manager-status":  {
        color: status_to_color[manager.status], 
        label: status_to_readable[manager.status],
      } as const
  }))
  )
  
);
</script>

<style lang="css" scoped>

</style>