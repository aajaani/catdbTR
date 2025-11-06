<script setup lang="ts">
import BreadCrumbs from "@/components/organisms/BreadCrumbs.vue";
import FilterTable from "@/components/organisms/FilterTable.vue";

import { MdArrowOutward } from "vue-icons-plus/md";
import { FiEdit3, FiX } from "vue-icons-plus/fi";
import { HiOutlineTrash } from "vue-icons-plus/hi";
import { AiOutlinePlus } from "vue-icons-plus/ai";

import { defineTable, field } from "@/components/FilterTable";

import Button from "@/components/atoms/Button.vue";

import TableText from "@/components/atoms/filter-table/Text.vue"
import TableStatus from "@/components/atoms/filter-table/Status.vue"

import Actions from "@/components/molecules/filter-table/Actions.vue";
import { computed, ref, watch } from "vue";

import api from "@/api_fetch.js";
import type { CatRead } from "@/gen_types/types.gen";
import { useRouter } from "vue-router";
import { useToast } from "primevue";

const router = useRouter( );
const toast = useToast( );

const isEditing = ref< number >( -1 );

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

const searchQuery = ref("");

const filteredEntries = computed(() => {
  if (!searchQuery.value.trim()) return tableDefinition.value.entries; // if search is empty, show all cats

  const search = searchQuery.value.toLowerCase();

  return tableDefinition.value.entries.filter(entry => { // check each row
    return Object.values(entry).some(cell => { // check for each cell in row and if at least one match, include it
      if (typeof cell === "object" && cell !== null) { //if its an object, check the values. Right now the mock data has objects
        return Object.values(cell).some(v =>
          typeof v === "string" && v.toLowerCase().includes(search) //check for strings inside objects that match search
        );
      }
      return typeof cell === "string" && cell.toLowerCase().includes(search); //if already strings, check if they match search
    });
  });
});

const CAT_STATUSES = [ "ACTIVE", "FOSTER", "ADOPTED", "ARCHIVED", "MISSING", "RESERVED" ] as const;
type CAT_STATUS_COLORS = "green" | "yellow" | "red" | "black" | "gray";

const status_to_color: { [ key in CatRead[ "status" ] ]: CAT_STATUS_COLORS } = {
  "ACTIVE": "yellow",
  "FOSTER": "yellow",
  "ADOPTED": "green",
  "ARCHIVED": "black",
  "MISSING": "red",
  "RESERVED": "gray"
}

const status_to_readable: { [ key in CatRead[ "status" ] ]: string } = {
  "ACTIVE": "Otsib kodu",
  "FOSTER": "Ajutises kodus",
  "ADOPTED": "Uues kodus",
  "ARCHIVED": "Kiisudemaal",
  "MISSING": "Kadunud",
  "RESERVED": "Broneeritud"
} 

const cats = ref< CatRead[ ] >([ ]);

// todo: refactor to something similiar to tanstack query
api.listCatsCatsGet( ).then( res => {
  console.log( "listCatsCatsGet: ", res );
  cats.value = res.data;
} )

const isEditingCat = ( cat: CatRead ) => {
  return isEditing.value === cat.id;
}

const pushCatEdit = ( cat: CatRead, body: Partial< CatRead > ) => {
  api.updateCatCatsCatIdPatch({
    body: {
      payload: JSON.stringify( body )
    },
    path: {
      cat_id: cat.id
    }
  }).then( res => {
    Object.assign( cat, res.data );
    isEditing.value = -1;
  }).catch( _ => {
    isEditing.value = -1;
    toast.add({
      severity: 'error',
      summary: 'Viga',
      detail: 'Kassi uuendamine ebaõnnestus',
      life: 3000
    });
  } )
}

const cancelEdit = ( ) => {
  isEditing.value = -1;
}

const tableDefinition = computed( ( ) => defineTable({
    "cat-intake-date": field({
      title: "KK alates",
      component: TableText,
      centerEntries: true,
      centerTitle: true
    }),
    "cat-name": field({
      title: "Kassi nimi",
      component: TableText,
    }),
    "cat-status": ({
      title: "Staatus",
      component: TableStatus,
      fitContent: true,
      filterMode: "unique",
      filterInputOptions: ( [ "ACTIVE", "FOSTER", "ADOPTED", "ARCHIVED", "MISSING", "RESERVED" ] as CatRead[ "status" ][ ] ).map( s => ({
        component: TableStatus,
          props: {
            color: status_to_color[ s ],
            label: status_to_readable[ s ],
          },
          searchName: status_to_readable[ s ]
      }))
    }),
    "cat-manager-name": field({
      title: "Vabatahtlik",
      component: TableText,
      fitContent: true,
      filterMode: "unique",
      filterInputOptions: [ "aaaa", "bbbb", "cccc" ]
    }),
    "cat-colony": field({
      title: "Originaalne koloonia",
      component: TableText,
    }),
    "cat-details": field({
      title: "Teated",
      component: TableText,
    }),
    "cat-on-homepage": field({
      title: "Kodukal",
      component: TableStatus,
    }),
    "cat-actions": field({
      title: "Tegevused",
      component: Actions,
      disableSorting: true
    })
  },
  cats.value.map( ( cat: CatRead ) => ({
    "cat-intake-date": {
      text: cat.intake_date ?? "-"
    } as const,
    "cat-name": {
      text: cat.name,
      isEditing: isEditingCat( cat ),
      onEditAccept: ( newText: string ) => pushCatEdit( cat, { name: newText } ),
      onEditCancel: ( ) => cancelEdit( )
    } as const,
    "cat-status": {
      color: status_to_color[ cat.status ],
      label: status_to_readable[ cat.status ],
      isEditing: isEditingCat( cat ),
      options: CAT_STATUSES.map( s => ({
        [ s ]: status_to_readable[ s ]
      }) ).reduce( ( acc, curr ) => ( { ...acc, ...curr } ), { } ) ,
      onChange: ( newCodeName: string, newPrettyName: string ) => pushCatEdit( cat, { status: newCodeName as CatRead[ "status" ] } )
    } as const,
    "cat-manager-name": {
      text: cat.manager?.display_name || "-",
    } as const,
    "cat-colony": {
      text: cat.colony ? cat.colony.name  : "-"
    } as const,
    "cat-details": {
      text: cat.notes ?? "-"
    } as const,
    "cat-on-homepage": {
      color: Math.random( ) > .5 ? "green" : "red"
    } as const,
    "cat-actions": {
      actions: [{
        icon: MdArrowOutward,
        onClick: ( ) => { router.push( `/cats/${ cat.id }` ) }
      }, {
        icon: isEditing.value == cat.id ? FiX : FiEdit3,
        onClick: ( ) => {
          if ( isEditing.value == -1 )
            isEditing.value = cat.id;
          else
            isEditing.value = -1;
        }
      }, {
        icon: HiOutlineTrash,
        onClick: ( ) => { }
      }]
    }
  }))
) );
</script>

<template>
  <div class="flex flex-col bg-main-bg px-8 py-4 gap-8">
    <div class="flex flex-col">
      <!-- todo: kinda overlaps with collapse/back button -->
      <h1 class="abril-fatface-regular text-[46px]">Kassid</h1>
      <BreadCrumbs />
    </div>

    <div class="flex flex-col gap-4 pt-2">
      <div class="flex flex-row justify-between">
        <router-link to="/add-cat">
          <Button class="primary border-0.5 text-primary-normal fill-neutral-white">
            <AiOutlinePlus size="20" class="fill-inherit"></AiOutlinePlus>
            Lisa kass
          </Button>
        </router-link>
        <input
            v-model="searchQuery"
            type="text"
            placeholder="Otsi"
            class="border border-gray-300 rounded-lg p-2 w-80 max-w-80 focus:outline-none focus:ring-2 focus:ring-gray-400"
          />
      </div>
      

      <FilterTable
        :fields="tableDefinition.fields"
        :entries="filteredEntries"
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
  </div>
</template>

<style scoped>

</style>