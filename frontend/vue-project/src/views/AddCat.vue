<template>
  <div class="flex flex-col bg-main-bg px-8 pt-4">
    <h1 class="abril-fatface-regular text-[46px]">Kassid</h1>
    <BreadCrumbs />

    <!-- todo: file list on the right, different layout on smaller screens -->
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
          <div class="flex flex-col col-start-1 col-span-4 row-end-1">
            <label for="cat-name">Kassi nimi</label>
            <input id="cat-name" name="cat-name" class="input" v-model="catData.name" required></input>
          </div>

          <!-- todo: implement colonies -->
          <div class="flex flex-col col-start-5 col-span-4 row-end-1">
            <label for="cat-colony">Originaalne koloonia</label>
            <input id="cat-colony" name="cat-colony" class="input" disabled></input>
          </div>

          <div class="flex flex-col col-start-9 col-span-4 row-end-1">
            <label for="cat-birth-date">Sunnikuupäev</label>
            <input id="cat-birth-date" name="cat-birth-date" type="date" class="input" v-model="catData.birthDate"></input>
          </div>

          <div class="flex flex-col col-start-1 col-span-2 row-end-2">
            <label for="cat-sex">Sugu</label>
            <HorizontalSingleSelection
              id="cat-sex"
              group-name="cat-sex"
              class="col-start-1 col-span-2 "
              fallback="unknown"
              v-model="catData.sex"
              :items="{
                'male': {
                  component: BiMaleSign,
                  props: { size: 20 }
                },
                'female': {
                  component: BiFemaleSign,
                  props: { size: 20 }
                }
              }"
            />
          </div>

          <div class="flex flex-col col-start-3 col-span-2 row-end-2">
            <label for="cat-on-homepage">Kodukal</label>
            <HorizontalSingleSelection
              id="cat-on-homepage"
              group-name="cat-on-homepage"
              class="col-start-1 col-span-2"
              v-model="catData.onHomepage"
              :items="{
                true: {
                  component: CgCheck,
                  props: { size: 24 }
                },
                false: {
                  component: CgClose,
                  props: { size: 20 }
                }
              }"
            />
          </div>

          <div class="flex flex-col col-start-5 col-span-4 row-end-2">
            <label for="cat-status">Staatus</label>
            <select id="cat-status" name="cat-status" class="input" @change="( e ) => {
                if ( !e.target ) return;
                const sel: CatRead[ 'status' ] | string = ( e.target as HTMLSelectElement ).value;
                if ( sel in catStatuses ) {
                  catData.status = sel as CatRead[ 'status' ];               
                } else {
                  console.error( `'${ sel }' not in cat statuses` );
                };
            }">
              <option
                v-for="( visualName, value ) in catStatuses"
                :value="value"
                :key="visualName"
              >{{ visualName }}</option>
            </select>
          </div>

          <div class="flex flex-col col-start-9 col-span-4 row-end-2">
            <label for="cat-chip-id">Kiibinumber</label>
            <NumberInput
              id="cat-chip-id"
              name="cat-chip-id"
              default=""
              :numbers="15"
              class="input"
              title="15 numbri pikkune kiibi number"
              v-model="catData.chipID"
            />
            <p class="text-[12px] text-text-secondary">Kiibinumber peaks olema 15 numbrit</p>
          </div>

          <div class="grid grid-rows-[auto_1fr] col-start-1 col-span-12 row-end-3 gap-2">
            <h1 class="col-start-1 col-span-3 text-2xl h-fit">KK alates</h1>
            <div class="col-start-1 col-span-3 flex flex-row gap-5">
              <div class="flex flex-col basis-1/3">
                <label for="cat-home-since">Kuupäev</label>
                <input id="cat-home-since" name="cat-home-since" type="date" class="input" v-model="catData.intakeDate"></input>
              </div>
              <!-- todo: manager dropdown -->
              <div class="flex flex-col basis-2/3">
                <label for="cat-manager">Haldur</label>
                <select id="cat-manager" name="cat-manager"
                  class="input"
                  @change="( e ) => {
                    if ( !e.target ) return;
                    const sel = ( e.target as HTMLSelectElement ).value;

                    try {
                      const selNum = parseInt( sel );
                      catData.managerId = selNum;
                    } catch ( _ ) {
                      console.error( `'${ sel }' not in managers (parseInt failure or wv)` );
                    };
                }">
                >
                  <option
                    key="manager-unassigned"
                    :value="-1"
                  >-</option>

                  <option
                      v-for="manager in managers"
                      :key="manager.id"
                      :value="manager.id"
                  >{{ manager.display_name }}</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </AccordionWithTitle>

      <!-- todo: could be that we have an existing foster home -->
      <!-- overall have to redo this part -->
      <AccordionWithTitle
        title="Hoiukodu info"
        :default-opened="true"
        class="bg-neutral-white rounded-lg"
      >
        <div class="grid grid-cols-2 gap-5">
          <div class="flex flex-col col-start-1 col-span-2">
            <label for="foster-home-selection">Hoiukodu valik</label>
            <select id="foster-home-selection" name="foster-home-selection"
              class="input"
              @change="( e ) => {
                if ( !e.target ) return;
                const sel = ( e.target as HTMLSelectElement ).value;

                try {
                  const selNum = parseInt( sel );
                  catData.fosterHomeId = selNum;
                } catch ( _ ) {
                  console.error( `'${ sel }' not in cat statuses` );
                };
            }">
            >
              <option
                key="new-home"
                :value="-1"
              >Uus hoiukodu</option>

              <option
                  v-for="fosterHome in fosterHomes"
                  :key="fosterHome.id"
                  :value="fosterHome.id"
              >{{ fosterHome.name || `Hoiukodu ${ fosterHome.id }` }}</option>
            </select>
          </div>

          <div
            v-if="catData.fosterHomeId === -1"
            class="flex flex-col col-start-1 col-span-1"
          >
            <label for="foster-home-name">Hoiukodu nimi</label>
            <input id="foster-home-name" name="foster-home-name" class="input" v-model="newFosterHomeData.name" required></input>
          </div>

          <div
            v-if="catData.fosterHomeId === -1"
            class="flex flex-col col-start-2 col-span-1"
          >
            <label for="foster-home-tel">Hoiukodu telefoninumber</label>
            <input id="foster-home-tel" name="foster-home-tel" class="input" type="tel" v-model="newFosterHomeData.phone"></input>
          </div>

          <div
            v-if="catData.fosterHomeId === -1"
            class="flex flex-col col-start-1 col-span-1"
          >
            <label for="foster-home-address">Hoiukodu aadress</label>
            <input id="foster-home-address" name="foster-home-address" class="input" v-model="newFosterHomeData.address"></input>
          </div>

          <div
            v-if="catData.fosterHomeId === -1"
            class="flex flex-col col-start-2 col-span-1"
          >
            <label for="foster-home-email">Hoiukodu e-mail</label>
            <input id="foster-home-email" name="foster-home-email" class="input" type="email" v-model="newFosterHomeData.email"></input>
          </div>

          <div
            v-if="catData.fosterHomeId === -1"
            class="flex flex-col col-start-1 col-span-2"
          >
            <label for="foster-home-address">Hoiukodu märkused</label>
            <textarea id="foster-home-details" name="foster-home-details" class="input" v-model="newFosterHomeData.notes"></textarea>
          </div>
        </div>
      </AccordionWithTitle>

      <AccordionWithTitle
        title="Meditsiiniline info"
        :default-opened="true"
        :lock="false"
        class="bg-neutral-white rounded-lg"
      >
        <div class="grid grid-cols-1">
          <TabSelection
            :tabs="[ 'Ussitablett', 'Turjatilk', 'Vaktsiin', 'Steriliseeritud' ]"
          >
            <template v-slot:Ussitablett>
              <div class="grid grid-cols-2 px-4 py-4 gap-5">
                <div class="flex flex-col col-start-1 col-span-1">
                  <label for="deworm-tablet-given-date">Andmise kuupäev</label>
                  <input id="deworm-tablet-given-date" name="deworm-tablet-given-date" type="date" class="input"></input>
                </div>

                <div class="flex flex-col col-start-2 col-span-1">
                  <label for="deworm-tablet-next-date">Järgmise võtmise kuupäev</label>
                  <input id="deworm-tablet-next-date" name="deworm-tablet-next-date" type="date" class="input"></input>
                </div>
              </div>
            </template>

            <template v-slot:Turjatilk>
              <div class="grid grid-cols-2 px-4 py-4 gap-5">
                <div class="flex flex-col col-start-1 col-span-1">
                  <label for="flea-drop-given-date">Andmise kuupäev</label>
                  <input id="flea-drop-given-date" name="flea-drop-given-date" type="date" class="input"></input>
                </div>

                <div class="flex flex-col col-start-2 col-span-1">
                  <label for="flea-drop-next-date">Järgmise võtmise kuupäev</label>
                  <input id="flea-drop-next-date" name="flea-drop-next-date" type="date" class="input"></input>
                </div>
              </div>
            </template>

            <template v-slot:Vaktsiin>
              <div class="grid grid-cols-2 px-4 py-4 gap-5">
                <div class="flex flex-col col-start-1 col-span-1">
                  <label for="vaccine-given-date">Andmise kuupäev</label>
                  <input id="vaccine-given-date" name="vaccine-given-date" type="date" class="input"></input>
                </div>

                <div class="flex flex-col col-start-2 col-span-1">
                  <label for="vaccine-next-date">Jargmise votmise kuupaev</label>
                  <input id="vaccine-next-date" name="vaccine-next-date" type="date" class="input"></input>
                </div>
              </div>
            </template>

            <template v-slot:Steriliseeritud>
              <div class="grid grid-cols-2 px-4 py-4 gap-5">
                <!-- todo: yes/no is mapped to isNeutered (bool|string now, only bool would be cool) -->
                <HorizontalSingleSelection
                  id="cat-sterilized"
                  group-name="cat-sterilized"
                  :items="{
                    true: 'Jah',
                    false: 'Ei'
                  }"
                  v-model="catData.isNeutered"
                  class="col-start-1 col-span-1"
                />

                <input type="date" class="input" :disabled="!catData.isNeutered"></input>
              </div>
            </template>
          </TabSelection>
        </div>
      </AccordionWithTitle>

      <AccordionWithTitle
        title="Märkmed"
        :default-opened="false"
        :lock="false"
        class="bg-neutral-white rounded-lg"
      >
        <textarea
          id="cat-details"
          name="cat-details"
          class="w-full resize-y input min-h-10"
          v-model="catData.notes"
        ></textarea>

      </AccordionWithTitle>

      <div class="flex justify-end mb-5 mt-auto">
        <div class="flex w-fit bg-neutral-white rounded-lg p-4 gap-5">
          <Button type="button">Tühista</Button>
          <Button class="secondary" type="reset">Tühjenda Väljad</Button>
          <Button class="primary" type="submit">Loo</Button>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import HorizontalSingleSelection from '@/components/atoms/HorizontalSingleSelection.vue';
import NumberInput from '@/components/atoms/NumberInput.vue';
import AccordionWithTitle from '@/components/molecules/AccordionWithTitle.vue';
import BreadCrumbs from '@/components/organisms/BreadCrumbs.vue';
import TabSelection from '@/components/organisms/TabSelection.vue';
import Button from '@/components/atoms/Button.vue';
import { ref, reactive } from 'vue';

import { BiMaleSign, BiFemaleSign } from 'vue-icons-plus/bi';
import { CgCheck, CgClose } from 'vue-icons-plus/cg';
import useVuelidate from '@vuelidate/core';
import { required, helpers } from '@vuelidate/validators';

import api from "@/api_fetch.js"
import {type UserRead, type CatRead, type FosterHomeRead, type ColonyRead} from '@/gen_types/types.gen';
import { useRouter } from "vue-router";

const router = useRouter( )

const catStatuses: { [ key: CatRead[ "status" ] ]: string } = {
  "ACTIVE": "Otsib kodu",
  "FOSTER": "Ajutises kodus",
  "ADOPTED": "Uues kodus",
  "ARCHIVED": "Kiisudemaal",
  "MISSING": "Kadunud",
  "RESERVED": "Broneeritud"
};

const fosterHomes = ref< FosterHomeRead[ ] >([ ]);
const managers = ref< UserRead[ ] >([ ]);
const colonies = ref< ColonyRead[ ] >([ ]);

// tanstack query-like lib could help us invalidate cache
// when we create a new cat. Right now when something goes wrong after
// foster home creation (cat creation), foster home is created, this
// isnt updated, next req same foster home will br created
// invalidating foster home cache on cat add fail would solve this issue
api.listFosterHomesFosterHomesGet( ).then( ( res ) => {
  // todo: error handleing
  fosterHomes.value = res.data;
});

api.listManagersManagersGet( ).then( res => {
  managers.value = res.data;
})

// todo: maybe add localStorage so when page is switched, form data isnt lost
const catData = reactive({
  name: "" as string,
  // todo: colony_id: "",
  birthDate: undefined as CatRead[ "birth_date" ],
  sex: "unknown",
  onHomepage: "true", // can't do booleans due to how HorizontalSingleSelection works
  chipID: "",
  intakeDate: undefined,
  status: "ACTIVE" as CatRead[ "status" ],
  managerId: -1,
  fosterHomeId: -1,
  // todo: foster_end_date
  notes: "",
  isNeutered: "false",
});

const newFosterHomeData = reactive({
  name: "",
  phone: "",
  address: "",
  email: "",
  notes: "",
});

// https://vuelidate-next.netlify.app/#alternative-syntax-composition-api
const validationRules = {
  name: { required: helpers.withMessage( "Name is required.", required ) },
  birthDate: {
    required: helpers.withMessage(
      "Date or empty",
      ( date: string ) => !date || !Number.isNaN( Date.parse( date ) )
    )
  },
  sex: { },
  onHomepage: { },
  chipID: { required: helpers.withMessage(
    "Chip ID must be unset or a 15 number string.",
    ( id: string ) => !id || /^\d{15}$/.test( id ) )
  },
  intakeDate: { },
  notes: { },
  isNeutered: { }
}

const v$ = useVuelidate( validationRules, catData );


const onSubmit = async ( e: SubmitEvent ) => {
  if ( !e.target ) return;

  const isFormValid = await v$.value.$validate( );

  console.log( v$.value )
  if ( !isFormValid ) return;

  if ( catData.fosterHomeId === -1 ) {
    // create foster 
    const newFosterHomeID = await sendFosterHomeCreate( );

    // no foster created, dont create cat
    // todo: show error
    if ( !newFosterHomeID ) return;

    catData.fosterHomeId = newFosterHomeID;
  }

  const catId = await sendCatCreate( );

  await router.push({
    name: "CatProfile",
    params: { id: catId }
  });
}

const sendFosterHomeCreate = async ( ): Promise< number > => {
  const res = await api.createFosterHomeFosterHomesPost({
    body: {
      name: newFosterHomeData.name,
      phone: newFosterHomeData.phone,
      email: newFosterHomeData.email,
      address: newFosterHomeData.address,
      comments: newFosterHomeData.notes
    }
  });

  // todo error validation;
  return res.data.id;
}

const sendCatCreate = async ( ) => {
  const sendData = {
    name: catData.name,
    // string enum: male | female | unknown (default unknown)
    sex: catData.sex,
    chip_number: catData.chipID,
    status: catData.status,
    // could have an unassigned manager aka -1, set to null if its -1
    manager_id: catData.managerId === -1 ? null : catData.managerId,
    // set in fosterhome creation anyways, always exists
    foster_home_id: catData.fosterHomeId,
    colony_id: null,
    intake_date: catData.intakeDate,
    birth_date: catData.birthDate,
    foster_end_date: null, // backend optional, idk if we'll use it yet
    notes: catData.notes,
    // backend expects bool
    is_neutered: catData.isNeutered === "true"
  }

  const formData = new FormData( );
  formData.append( "payload", JSON.stringify( sendData ) );

  const res = await api.createCatCatsPost({
    body: { payload: JSON.stringify( sendData ) }
  });

  return res.data.id;
}
</script>

<style lang="css" scoped>
#cat-sex:deep( .item-container ) {
    &:first-child:has( input:checked ) {
      @apply bg-sex-male border-sex-male border-[color-mix(in_srgb,theme(colors.sex.male)_90%,black)];
    }
    
    /* female selected */
    &:last-child:has( input:checked ) {
      @apply bg-sex-female border-[color-mix(in_srgb,theme(colors.sex.female)_90%,black)];
    }
    /* need to apply right border for male and set it as it is above */
    &:first-child:has( + & input:checked ) {
      @apply border-r-[color-mix(in_srgb,theme(colors.sex.female)_90%,black)];
    }
}


#cat-on-homepage:deep( .item-container ) {
  &:first-child:has( input:checked ) {
    @apply bg-[#66e16660] border-sex-male border-[color-mix(in_srgb,#66e166_90%,black)];
  }
    
  /* female selected */
  &:last-child:has( input:checked ) {
    @apply bg-[#fd35357e] border-[color-mix(in_srgb,#fd3535_90%,black)];
  }
  /* need to apply right border for male and set it as it is above */
  &:first-child:has( + & input:checked ) {
    @apply border-r-[color-mix(in_srgb,#fd3535_90%,black)]
  }
}

#cat-sterilized:deep( .item-container ) {
  &:first-child:has( input:checked ) {
    @apply bg-[#66e16660] border-sex-male border-[color-mix(in_srgb,#66e166_90%,black)];
  }
    
  /* female selected */
  &:last-child:has( input:checked ) {
    @apply bg-[#fd35357e] border-[color-mix(in_srgb,#fd3535_90%,black)];
  }
  /* need to apply right border for male and set it as it is above */
  &:first-child:has( + & input:checked ) {
    @apply border-r-[color-mix(in_srgb,#e16666_90%,black)]
  }
}
</style>