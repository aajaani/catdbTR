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
import TableSelection from "@/components/atoms/filter-table/Selection.vue"
import { useRouter } from "vue-router";
import api from '@/api_fetch';
import { type UserRead } from "@/gen_types/types.gen.ts";

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

type ActivityStatus = "ACTIVE" | "INACTIVE";

const get_activity_status = (user: UserRead): ActivityStatus => {
  return user.is_active ? "ACTIVE" : "INACTIVE";
}

// todo: stricter types
// right now we're not accounting for undefined
const status_to_color: Record<ActivityStatus, 'green' | 'red'> = {
  ACTIVE: 'green',
  INACTIVE: 'red',
};
const status_to_readable: Record<ActivityStatus, string> = {
  ACTIVE: 'Aktiivne',
  INACTIVE: 'Mitte aktiivne',
};

const role_to_readable: Record<UserRead["role"]["name"], string> = {
  MANAGER: 'Haldur',
  NOT_MANAGER: 'Pole haldur',
};

const managers = ref< UserRead[ ] >([ ]);

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
      component: TableSelection,
      fitContent: true,
      filterMode: "unique",
      filterInputOptions: ( ['ACTIVE', 'INACTIVE'] as ActivityStatus[] ).map((s) => ({
        component: TableSelection,              // or TableStatus with { color, label }
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
    managers.value.map(( manager: UserRead) => ({
      "manager-id": {
        text: String(manager.id)
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
        text: manager.role.name
      } as const,
      "manager-status":  {
        color: status_to_color[get_activity_status(manager)],
        label: status_to_readable[get_activity_status(manager)],
      } as const
  }))
  )
  
);
</script>

<style lang="css" scoped>

</style>