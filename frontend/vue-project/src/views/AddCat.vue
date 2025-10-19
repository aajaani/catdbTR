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
        title="Uldine"
        :default-opened="true"
        :lock="true"
        class="bg-neutral-white rounded-lg px-4 py-4"
      >
        <div class="grid grid-cols-12 gap-5 ">
          <div class="flex flex-col col-start-1 col-span-4 row-end-1">
            <label for="cat-name">Kassi nimi</label>
            <input id="cat-name" name="cat-name" class="input" v-model="catData.name" required></input>
          </div>

          <div class="flex flex-col col-start-5 col-span-4 row-end-1">
            <label for="cat-colony">Originaalne koloonia</label>
            <input id="cat-colony" name="cat-colony" class="input" v-model="catData.colony"></input>
          </div>

          <div class="flex flex-col col-start-9 col-span-4 row-end-1">
            <label for="cat-birth-date">Sunnikuupaev</label>
            <input id="cat-birth-date" name="cat-birth-date" type="date" class="input" v-model="catData.birthDate"></input>
          </div>

          <div class="flex flex-col col-start-1 col-span-3 row-end-2">
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

          <div class="flex flex-col col-start-4 col-span-3 row-end-2">
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

          <div class="flex flex-col col-start-7 col-span-6 row-end-2">
            <label for="cat-chip-id">Kiibi number</label>
            <NumberInput
              id="cat-chip-id"
              name="cat-chip-id"
              default=""
              :numbers="15"
              class="input"
              title="15 numbri pikkune kiibi number"
              v-model="catData.chipID"
            />
            <p class="text-[12px] text-text-secondary">Kiibi number peaks olema 15 numbrit</p>
          </div>

          <div class="grid grid-rows-[auto_1fr] col-start-1 col-span-12 row-end-3 gap-2">
            <h1 class="col-start-1 col-span-3 text-2xl h-fit">KK alates</h1>
            <div class="col-start-1 col-span-3 flex flex-row gap-5">
              <div class="flex flex-col basis-1/3">
                <label for="cat-home-since">Kuupaev</label>
                <input id="cat-home-since" name="cat-home-since" type="date" class="input" v-model="catData.intakeDate"></input>
              </div>
              <!-- todo: manager dropdown -->
              <div class="flex flex-col basis-2/3">
                <label for="cat-manager">Haldur</label>
                <input id="cat-manager" name="cat-manager" type="text" class="input"></input>
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
          <div class="flex flex-col col-start-1 col-span-1">
            <label for="foster-home-name">Hoiukodu nimi</label>
            <input id="foster-home-name" name="foster-home-name" class="input col-start-1 col-span-1"></input>
          </div>

          <div class="flex flex-col col-start-2 col-span-1">
            <label for="foster-home-tel">Hoiukodu telefoninumber</label>
            <input id="foster-home-tel" name="foster-home-tel" class="input col-start-2 col-span-1" type="tel"></input>
          </div>

          <div class="flex flex-col col-start-1 col-span-2 row-start-2">
            <label for="foster-home-address">Hoiukodu aadress</label>
            <input id="foster-home-address" name="foster-home-address" class="input col-start-2 col-span-1" type="tel"></input>
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
                  <label for="deworm-tablet-given-date">Andmise kuupaev</label>
                  <input id="deworm-tablet-given-date" name="deworm-tablet-given-date" type="date" class="input"></input>
                </div>

                <div class="flex flex-col col-start-2 col-span-1">
                  <label for="deworm-tablet-next-date">Jargmise votmise kuupaev</label>
                  <input id="deworm-tablet-next-date" name="deworm-tablet-next-date" type="date" class="input"></input>
                </div>
              </div>
            </template>

            <template v-slot:Turjatilk>
              <div class="grid grid-cols-2 px-4 py-4 gap-5">
                <div class="flex flex-col col-start-1 col-span-1">
                  <label for="flea-drop-given-date">Andmise kuupaev</label>
                  <input id="flea-drop-given-date" name="flea-drop-given-date" type="date" class="input"></input>
                </div>

                <div class="flex flex-col col-start-2 col-span-1">
                  <label for="flea-drop-next-date">Jargmise votmise kuupaev</label>
                  <input id="flea-drop-next-date" name="flea-drop-next-date" type="date" class="input"></input>
                </div>
              </div>
            </template>

            <template v-slot:Vaktsiin>
              <div class="grid grid-cols-2 px-4 py-4 gap-5">
                <div class="flex flex-col col-start-1 col-span-1">
                  <label for="vaccine-given-date">Andmise kuupaev</label>
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
        title="Markmed"
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
          <Button type="button">Tuhista</Button>
          <Button class="secondary" type="reset">Tuhjenda Valjad</Button>
          <Button class="primary" type="submit">Loo</bUtToN>
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
import { required, helpers, minLength } from '@vuelidate/validators';

import { createCatCatsPost } from "@/gen_types/sdk.gen"

// todo: maybe add localStorage so when page is switched, form data isnt lost
const catData = reactive({
  name: "",
  // todo: colony_id: "",
  birthDate: undefined,
  sex: "unknown",
  onHomepage: "true", // can't do booleans due to how HorizontalSingleSelection works
  chipID: "",
  intakeDate: undefined,
  // todo: manager_id
  // todo: status
  // todo: foster_home_id (name, id, address)
  // todo: foster_end_date
  notes: "",
  isNeutered: "false",
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

  const sendData = {
    name: catData.name,              // • string (unique)
    sex: catData.sex,             // string enum: male | female | unknown (default unknown)
    chip_number: catData.chipID,             // string?
    status: "ACTIVE",              // enum: ACTIVE | FOSTER | ADOPTED | ARCHIVED | MISSING | RESERVED (default ACTIVE)
    manager_id: null,              // int?
    foster_home_id: null,              // int?
    colony_id: null,             // int?
    intake_date: catData.intakeDate,             // date?
    birth_date: catData.birthDate,              // date?
    foster_end_date: null,             // date?
    notes: catData.notes,             // string?
    is_neutered: catData.isNeutered === "true",             // bool?
  }


  const formData = new FormData( );
  formData.append( "payload", JSON.stringify( sendData ) );

  createCatCatsPost({
    body: { payload: JSON.stringify( sendData ) }
  });
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