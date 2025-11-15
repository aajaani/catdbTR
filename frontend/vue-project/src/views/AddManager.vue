<template>
  <div class="flex flex-col bg-main-bg px-8 pt-4">
    <h1 class="abril-fatface-regular text-[46px]">Lisa Vabatahtlik</h1>
    <BreadCrumbs />
 

    <form
          class="flex flex-col gap-8 abyssinica-sil-regular mt-8 flex-1"
          @submit.prevent="onSubmit"
    >
     <AccordionWithTitle
        title="Üldine"
        :default-opened="true"
        :lock="true"
        class="bg-neutral-white rounded-lg px-4 py-4"
      >

        <div class="grid grid-cols-12 gap-5 ">
          <div class="flex flex-col col-start-1 col-span-6">
            <label for="volunteer-firstName">Eesnimi</label>
            <input id="volunteer-firstName" name="volunteer-firstName" class="input" v-model="form.firstName"  />
          </div>
          

          <div class="flex flex-col col-start-7 col-span-6">
            <label for="volunteer-lastName">Perekonnanimi</label>
            <input id="volunteer-lastName" name="volunteer-lastName" class="input" v-model="form.lastName"  />
          </div>

          <div class="flex flex-col col-start-1 col-span-6 ">
            <label for="volunteer-email">E-post</label>
            <input id="volunteer-email" name="volunteer-email" type="email" class="input" v-model="form.email"  />
          </div>

          <!--<div class="flex flex-col col-start-7 col-span-6 ">
            <label for="volunteer-password">Parool</label>
            <input id="volunteer-password" name="volunteer-password" type="password" class="input" v-model="form.password"  />
          </div>-->

          <div class="flex flex-col col-start-1 col-span-6">
            <label for="volunteer-phone-cc">Telefon</label>
            <div class="flex gap-3">
            <input id="phone-cc" class="input w-28" v-model="form.phoneCc" @input="sanitizeCc" placeholder="+372" />
            <input id="volunteer-phone" name="volunteer-phone" class="input" @input="acceptNumber" v-model="form.phoneNum" />
            </div>
          </div> 

          <div class="flex flex-col col-start-7 col-span-5">
            <label for="volunteer-role">Ametikoht</label>
            <HorizontalSingleSelection
            id="volunteer-role"
            group-name="volunteer-role"
            class="col-start-1 col-span-5"
            v-model="form.managerChoice"
            :items="{
              MANAGER: 'Haldur',
              NOT_MANAGER: 'Pole haldur'
            }"required>
            </HorizontalSingleSelection>
          </div>
        
      </div>
      </AccordionWithTitle>
      <div class="flex justify-end mb-5">
            <div class="flex w-fit bg-neutral-white rounded-lg p-4 gap-5">
              <Button type="button" @click="onCancel">Tühista</Button>
              <Button class="secondary" type="reset">Tühjenda Väljad</Button>
              <Button class="primary" type="submit">Loo</Button>
            </div>
        </div> 
    </form>
 </div>
</template>


<script setup lang="ts">
import {ref, reactive, onMounted, computed} from 'vue';
import BreadCrumbs from '@/components/organisms/BreadCrumbs.vue';
import Button from '@/components/atoms/Button.vue';
import AccordionWithTitle from '@/components/molecules/AccordionWithTitle.vue';
import { useRouter } from "vue-router";

import api from "@/api_fetch.js"
import type { RoleRead, UserRead } from '@/gen_types/types.gen';
import HorizontalSingleSelection from '@/components/atoms/HorizontalSingleSelection.vue';
import { useToast } from "primevue";


const router = useRouter( )
const toast = useToast( );

// backend role code types: 'ADMIN' | 'MANAGER' | 'SOCIAL_WORKER'
type UiManagerChoice = 'MANAGER' | 'NOT_MANAGER'


const form = reactive({
  firstName: '',
  lastName: '',
  email: '',
  phoneCc: '+372',
  phoneNum: '',
  //password: '',
  managerChoice: 'MANAGER' as UiManagerChoice,

})



//keeping digits only
function acceptNumber(e: Event) {
  const input = e.target as HTMLInputElement
  let out = ''
  for (const ch of input.value) if (ch >= '0' && ch <= '9') out += ch
  input.value = out
  form.phoneNum = out
}

function sanitizeCc(e: Event) {
  const input = e.target as HTMLInputElement
  let out = ''
  for (const ch of input.value) {
    if (ch >= '0' && ch <= '9') out += ch
    else if (ch === '+' && out.length === 0) out = '+'
  }
  input.value = out
  form.phoneCc = out

}

//always start with + has only digits international format for phone numbers
function toE164(cc: string, num: string) {
  const c = cc.split('').filter(ch => ch >= '0' && ch <= '9').join('')
  const n = num.split('').filter(ch => ch >= '0' && ch <= '9').join('')
  if ( !c || !n) {
    return null
  }
  return `+${c} ${n}`
  

}

function onCancel() {
  router.push('/users')
}

const roles = ref<RoleRead[]>([]);



onMounted(async () => {
  const {data, error} = await api.getAllRolesRolesGet({});
  console.log("GET /roles responses", {data, error});
  if (error) {
    console.error("Failed to load roles", error);
    toast.add({
      severity: "error",
      summary: "Viga",
      detail: "Rollide laadimine ebaõnnestus.",
      life: 3000,
    });
    return;
  }
  roles.value = data ?? [];

});

const managerRoleId = computed(() =>
  roles.value.find(r => r.name === "MANAGER")?.id ?? null
);

const socialWorkerRoleId = computed(() =>
  roles.value.find(r => r.name === "SOCIAL_WORKER")?.id ?? null
);

const sendVolunteerCreate = async ( ) => {
  const isManager = form.managerChoice === 'MANAGER'
  // I need to get the role id because i need to send for the post request the id not the name
  const roleId = isManager ? managerRoleId.value : socialWorkerRoleId.value;
  //not ceating ADMIN right now
  if (!roleId) {
    throw new Error('Rolli id puudub')
  }
  // usercreate contains: these fields
  const sendData = {
    username: form.email.trim(),
    display_name: `${form.firstName.trim()} ${form.lastName.trim()}`.trim(),
    phone: toE164(form.phoneCc, form.phoneNum) || null,
    email: form.email.trim(),
    password: '',
    role_id: roleId,
  };
  
  const res = await api.createUserFullUsersFullCreatePost({ body: sendData});
  if (res.error) {
    throw res;
  }
  return res.data?.id

}

const onSubmit = async (e: SubmitEvent) => {
  e.preventDefault();

  let hasError = false;

  if (!form.firstName.trim()) {
    toast.add({
                   severity: 'error',
                   summary: 'Ebaõnnestus',
                   detail: 'Kasutaja loomine ebaõnnestus. Eesnimi on kohustuslik.',
                   life: 3000
                 });
                 hasError = true;
  }

  if (!form.lastName.trim()) {
    toast.add({
                   severity: 'error',
                   summary: 'Ebaõnnestus',
                   detail: 'Kasutaja loomine ebaõnnestus. Perekonnanimi on kohustuslik.',
                   life: 3000
                 });
                  hasError = true;

  }
  if (!form.email.trim()) {
    toast.add({
                   severity: 'error',
                   summary: 'Ebaõnnestus',
                   detail: 'Kasutaja loomine ebaõnnestus. E-mail on kohustuslik.',
                   life: 3000
                 });
                  hasError = true;

  }
  if (!form.managerChoice.trim()) {
    toast.add({
                 severity: 'error',
                  summary: 'Ebaõnnestus',
                   detail: 'Kasutaja loomine ebaõnnestus. Rolli valimine on kohustuslik.',
                   life: 3000
                 });
                  hasError = true;
  }


  if(hasError) return;


  try {
    const id = await sendVolunteerCreate();
    await router.push('/users');
    toast.add({ severity: 'success', summary: 'Õnnestus', detail: 'Olete edukalt loonud kasutaja!', life: 3000 });

  } catch (err: any) {
  
    // Showing the error in console as well server one
    console.error(
    "Create manager failed:",
    err?.response?.status,
    err?.response?.statusText,
    err?.response?.data || err
  );

  const status = err?.response?.status;
  
    if (status === 409) {
      toast.add({
                   severity: 'error',
                   summary: 'Ebaõnnestus',
                   detail: 'Kasutaja loomine ebaõnnestus. Email on juba kasutatud.',
                   life: 3000
                 });
                  return;
    } else {
    toast.add({
      severity: 'error',
      summary: 'Ebaõnnestus',
      detail: 'Kasutaja loomine ebaõnnestus serveri vea tõttu.',
      life: 3000
    })
  }
  }
};


</script>

<style lang="css" scoped>

</style>