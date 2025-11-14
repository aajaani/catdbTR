<template>
  <!-- todo: could make the container a separate component to reduce rewrites for each view with breadcrumbs and title -->
  <div class="flex flex-col bg-main-bg px-8 pt-4">
    <h1 class="abril-fatface-regular text-[46px]">Vabatahtlikud</h1>
    <BreadCrumbs />

    <div class="flex flex-col gap-4 pt-2">
      <div class="flex flex-row justify-between">
        <router-link to="/add-user">
          <Button class="primary border-0.5 text-primary-normal fill-neutral-white">
            <AiOutlinePlus size="20" class="fill-inherit"></AiOutlinePlus>
            Lisa vabatahtlik
          </Button>
        </router-link>
        <input
            v-model="searchQuery"
            type="text"
            placeholder="Otsi"
            class="border border-gray-300 rounded-lg p-2 w-80 max-w-80 focus:outline-none focus:ring-2 focus:ring-gray-400"
          />
      </div>
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
</template>

<script setup lang="ts">
import { ref, watch, computed, onMounted } from 'vue';
import BreadCrumbs from '@/components/organisms/BreadCrumbs.vue';
import { defineTable, field } from "@/components/FilterTable.ts"
import FilterTable from "@/components/organisms/FilterTable.vue"
import TableText from "@/components/atoms/filter-table/Text.vue"
import TableSelection from "@/components/atoms/filter-table/Selection.vue"
import { useRouter } from "vue-router";
import api from '@/api_fetch';
import { type UserRead, type UserUpdate, type RoleRead, type DeleteUserUsersUserIdDeleteData } from "@/gen_types/types.gen.ts";
import Button from "@/components/atoms/Button.vue";
import { AiOutlinePlus } from "vue-icons-plus/ai";
import { FiEdit3, FiX } from "vue-icons-plus/fi";
import { HiOutlineTrash } from "vue-icons-plus/hi";
import { useToast } from "primevue";


import Actions from "@/components/molecules/filter-table/Actions.vue";
import { nodeModuleNameResolver } from 'typescript';




const router = useRouter( )
const toast = useToast( );

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

const isEditing = ref< number >( -1 );

const filteredEntries = computed(() => {
  if (!searchQuery.value.trim()) return tableDefinition.value.entries; 
  const search = searchQuery.value.toLowerCase();
  return tableDefinition.value.entries.filter(entry => { // check each row
    return Object.values(entry).some(cell => { // check for each cell in row and if at least one match, include it
      if (typeof cell === "object" && cell !== null) { //if its an object, check the values. Right now the mock data has objects
        return Object.values(cell).some(v =>
          typeof v === "string" && v.toLowerCase().includes(search) //check for strings inside objects that match search
        );
      }
      // @ts-ignore might be string actually, @sebastim can you check this ?
      return typeof cell === "string" && cell.toLowerCase().includes(search); //if already strings, check if they match search
    });
  });
});


type ActivityStatus = "ACTIVE" | "INACTIVE";
const ACTIVITY_STATUSES: ActivityStatus[] = ["ACTIVE", "INACTIVE"]

type IsManager = "Haldur" | "Pole haldur";

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
  SOCIAL_WORKER: 'Pole haldur',
  ADMIN: 'Admin',
};

const cancelEdit = ( ) => {
  isEditing.value = -1;
}

const isEditingUser = ( user: UserRead ) => {
  return isEditing.value === user.id;
}

const buildUserUpdateBody = (user: UserRead, patch: Partial<UserUpdate>): UserUpdate => ({
  display_name: patch.display_name ?? user.display_name ?? null,
  role_id: patch.role_id ?? user.role.id ?? null,
  is_active: patch.is_active ?? user.is_active, 
  phone: patch.phone ?? user.phone ?? null,
  email: patch.email ?? user.email,
})

const updateUser = async (user: UserRead, patch: Partial<UserUpdate>) => {
  try {
    const body: UserUpdate = buildUserUpdateBody(user, patch);
    const res = await api.editUserUsersUserIdPatch({
      path: { user_id: user.id },
      body,
    });

    if (!res.data) return;

    Object.assign(user, res.data);
    isEditing.value = -1;
    toast.add({
      severity: "success",
      summary: "Õnnestus",
      detail: "Kasutaja uuendatud!",
      life: 2000,
    });
  } catch (e) {
    isEditing.value = -1;
    toast.add({
      severity: "error",
      summary: "Viga",
      detail: "Kasutaja uuendamine ebaõnnestus.",
      life: 3000,
    });
    console.error(e);
  }
};

const deleteUser = async (user: UserRead) => {
  try {
    await api.deleteUserUsersUserIdDelete( {
      path: {user_id: user.id}
    })

    managers.value = managers.value.filter(u => u.id !== user.id);

    toast.add({
      severity: "success",
      summary: "Kustutatud", 
      detail: "Kasutaja eemaldatud",
      life: 3000,
    }) 
  } catch (e) {
    toast.add({
      severity: "error",
      summary: "Viga",
      detail: "Kasutaja kustutamine ebaõnnestus", 
      life: 3000
    });
    console.error(e)
  }
}

const managers = ref< UserRead[ ] >([ ]);
const visible_roles: UserRead["role"]["name"][] = ["MANAGER", "SOCIAL_WORKER"]

api.listUsersUsersGet().then( (res) => {
  console.log("RAW /users DATA:", res.data);
  managers.value = (res.data ?? []).filter(
    (user) => visible_roles.includes(user.role.name)
  );
});

const roles = ref<RoleRead[]>([]);
onMounted(async () => {
  const { data, error} = await api.getAllRolesRolesGet({});
  if (error) {
    console.error("Failed to load roles", error);
    toast.add({
      severity: "error", 
      summary: "Viga", 
      detail: "Rollide laadimine ebaõnnestus",
      life: 3000,
    });
    return;
  }
  roles.value = data ?? [];
});

const managerRoleId = computed(() =>
  roles.value.find(r => r.name === "MANAGER")?.id ?? null);

const socialWorkerRoleId = computed(() =>
  roles.value.find(r => r.name === "SOCIAL_WORKER")?.id ?? null);


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
        component: TableSelection,           
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
      component: TableSelection,
      fitContent: true,
      filterMode: "unique",
      filterInputOptions: ( ['Haldur', 'Pole haldur'] as IsManager[] ).map((s) => ({
        component: TableSelection,              // or TableStatus with { color, label }
        props: { 
          label: s,
        },
        searchName: s,
      })),
    }),
     "manager-actions": field({
      title: "Tegevused",
      component: Actions,
      disableSorting: true
    })


  };
  const tableDefinition = computed(() => defineTable(
    fields, 
    managers.value.map(( manager: UserRead) => ({
      "manager-id": {
        text: String(manager.id)
      } as const,
      "manager-name": {
        text: manager.display_name,
        isEditing: isEditingUser(manager),
        onEditAccept: (newText: string) => updateUser(manager, { display_name: newText}),
        onEditCancel: cancelEdit,
      } as const,
      "manager-phone": {
        text: manager.phone ?? "",
        isEditing: isEditingUser(manager),
        onEditAccept: (newPhone: string) => updateUser(manager, { phone: newPhone }),
        onEditCancel: cancelEdit,

      } as const,
      "manager-email": {
        text: manager.email ?? "",
        isEditing: isEditingUser(manager),
        onEditAccept: (newEmail: string) => updateUser(manager, { email: newEmail }),
        onEditCancel: cancelEdit,
      } as const,
      "manager-role": {
        label: role_to_readable[manager.role.name] ?? manager.role.name,
         isEditing: isEditingUser(manager),
         options: (() => {
          const opts: Record<string, number> = {};
          if (managerRoleId.value != null) {
            opts["Haldur"] = managerRoleId.value;
          } 
          if (socialWorkerRoleId.value != null) {
            opts["Pole haldur"] = socialWorkerRoleId.value
          }
          return opts;
         }) (),
         onChange: (key: string | number | boolean, _pretty: string) => {
          if (typeof key !== "number") return;
          void updateUser(manager, {role_id: key});
         },
      } as const,
      "manager-status":  {
        color: status_to_color[get_activity_status(manager)],
        label: status_to_readable[get_activity_status(manager)],
        isEditing: isEditingUser(manager),
        options: ACTIVITY_STATUSES.map( (s) => ({
          [status_to_readable[s]]: s,
        })).reduce(( acc, curr) => ({ ...acc, ...curr}), {} as Record<string, ActivityStatus>),
        onChange: (key: string | number | boolean, _pretty: string) => {
          const statusName = key as ActivityStatus;
          void updateUser(manager, { is_active: statusName === "ACTIVE"});
        },
      } as const,
      "manager-actions": {
        actions: [{
        icon: isEditing.value == manager.id ? FiX : FiEdit3,
        onClick: ( ) => {
          if ( isEditing.value == -1 )
            isEditing.value = manager.id;
          else
            isEditing.value = -1;
        }
        
      }, {
        icon: HiOutlineTrash,
        onClick: ( ) => deleteUser(manager)
      }]
    }
  }))
  )
  
);
</script>

<style lang="css" scoped>

</style>