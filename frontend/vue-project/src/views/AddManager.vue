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
            <input id="volunteer-firstName" name="volunteer-firstName" class="input" v-model="form.firstName" required />
          </div>
          

          <div class="flex flex-col col-start-7 col-span-6">
            <label for="volunteer-lastName">Perekonnanimi</label>
            <input id="volunteer-lastName" name="volunteer-lastName" class="input" v-model="form.lastName" required />
          </div>

          <div class="flex flex-col col-start-1 col-span-6 ">
            <label for="volunteer-email">E-post</label>
            <input id="volunteer-email" name="volunteer-email" type="email" class="input" v-model="form.email" required />
          </div>

          <div class="flex flex-col col-start-7 col-span-6">
            <label for="volunteer-phone-cc">Telefon</label>
            <div class="flex gap-3">
            <input id="phone-cc" class="input w-28" v-model="form.phoneCc" @input="sanitizeCc" placeholder="+372" required />
            <input id="volunteer-phone" name="volunteer-phone" class="input" @input="acceptNumber" v-model="form.phoneNum" required/>
            </div>
          </div> 

          <div class="flex flex-col col-start-1 col-span-5">
            <label for="volunteer-role">Ametikoht</label>
            <HorizontalSingleSelection
            id="volunteer-role"
            group-name="volunteer-role"
            class="col-start-1 col-span-5"
            v-model="form.role"
            :items="{
              MANAGER: volunteerRole.MANAGER,
              NOT_MANAGER: volunteerRole.NOT_MANAGER
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
import {ref, reactive} from 'vue';
import BreadCrumbs from '@/components/organisms/BreadCrumbs.vue';
import Button from '@/components/atoms/Button.vue';
import TabSelection from '@/components/organisms/TabSelection.vue';
import AccordionWithTitle from '@/components/molecules/AccordionWithTitle.vue';
import useVuelidate from '@vuelidate/core';
import { required, email as isEmail, helpers } from '@vuelidate/validators';
import { useRouter, type RouteLocation } from "vue-router";

import api from "@/api_fetch.js"
import type { ManagerRead } from '@/gen_types/types.gen';
import HorizontalSingleSelection from '@/components/atoms/HorizontalSingleSelection.vue';


const router = useRouter( )

// define the form state that v-model binds to
const volunteerRole: Record<ManagerRead['role'], string> = {
  MANAGER: 'Haldur',
  NOT_MANAGER: 'Pole haldur',
};
const volunteerStatuses: Record<ManagerRead['status'], string> = {
  ACTIVE: 'Aktiivne',
  INACTIVE: 'Pole aktiivne',
};

const form = reactive({
  firstName: '',
  lastName: '',
  email: '',
  phoneCc: '+372',
  phoneNum: '',
  role: 'MANAGER',
  status: 'ACTIVE'

})


// https://vuelidate-next.netlify.app/#alternative-syntax-composition-api
const validationRules = {
  firstName: { required: helpers.withMessage('Eesnimi on kohustuslik.', required) },
  lastName:  { required: helpers.withMessage('Perekonnanimi on kohustuslik.', required) },
  email: {
    required: helpers.withMessage('E-post on kohustuslik.', required),
    email:    helpers.withMessage('Palun sisesta korrektne e-posti aadress.', isEmail),
  },
  phoneCc: { required: helpers.withMessage('Riigikood on kohustuslik.', required) },
  phoneNum: { required: helpers.withMessage('Telefon on kohustuslik.', required) },
  role:     { required: helpers.withMessage('Ametikoht on kohustuslik.', required) },
}
const v$ = useVuelidate(validationRules, form)


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
  return `+${c}${n}`
}

function onCancel() {
  router.push('/managers')
}


const sendVolunteerCreate = async ( ) => {
  const sendData = {
    display_name: `${form.firstName.trim()} ${form.lastName.trim()}`.trim(),
    phone: toE164(form.phoneCc, form.phoneNum) || null,
    email: form.email.trim() || null,
    status: form.status,
    role: form.role,
  };
  const data = await api.createManagerManagersPost({ body: sendData });
  if (!data.data.id) throw new Error(`Missing id in response: ${JSON.stringify(data)}`);
  return data.data.id
};

const onSubmit = async (e: SubmitEvent) => {
   if (!e.target) return;
  const ok = await v$.value.$validate();
  if (!ok) return;

  try {
    const id = await sendVolunteerCreate();
    await router.push('/managers');
  } catch (err: any) {
    // Show the REAL server error (e.g., 403 Not authenticated)
    console.error(
      "Create manager failed:",
      err?.response?.status,
      err?.response?.statusText,
      err?.response?.data || err
    );
  }
};


</script>

<style lang="css" scoped>

</style>