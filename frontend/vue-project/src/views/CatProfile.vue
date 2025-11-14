<template>
    <div class="flex flex-col bg-cat-bg px-4 py-6 gap-8">
        <div class="relative flex flex-col z-1">
            <div
                class="absolute w-full h-[190px] bg-cat-header rounded-[10px] z-0"
            >
            </div>

            <div class="flex flex-col px-4 pt-12 z-10 gap-2">
                <BreadCrumbs class="light" />

                <div
                    v-if="catData?.id"
                    id="cat-info-container"
                    class="grid grid-cols-1 w-full 2md:grid-cols-2 xl:grid-rows-[auto_1fr] xl:grid-cols-[2fr_3fr] px-4 gap-5"
                >
                    <div class="col-start-1 xl:row-start-1 xl:row-span-2">
                        <div class="flex flex-col w-full bg-main-bg rounded-[10px] gap-4 px-3 py-3">
                            <div class="flex justify-center items-center">
                                <Status
                                    :color="status_to_color[ catData.status ]"
                                    :label="status_to_readable[ catData.status ]"
                                />
                            </div>
                            
                            <!-- cat heading info -->
                            <div
                                class="flex flex-row items-center gap-5"
                            >
                                <img
                                    class="w-[72px] h-[72px] rounded-full"
                                    src="https://picsum.photos/100/100"
                                    alt="cat-img"
                                ></img>

                                <h1 class="uppercase text-[18px] abril-fatface-regular">{{ catData.name }}</h1>

                                <Button class="mr-0 ml-auto small">
                                    Lae pilt ules
                                </Button>
                            </div>

                            <div
                                class="flex flex-col gap-2 edit-container"
                                :data-currently-editing="isEditing( 'main' )"
                            >
                                <div class="flex flex-row justify-between items-center">
                                    <h1 class="text-[18px] abril-fatface-regular">Peamine Info</h1>
                                    <Button
                                        class="justify-self-end small"
                                        @click="onClick( 'main' )"
                                    >
                                        {{ formatEditButtonText( "main" ) }}
                                    </Button>
                                </div>

                                <!-- main data fields -->
                                <div class="group outfit-400">
                                    <div class="infofield">
                                        <p>Nimi</p>
                                        <p class="capitalize">{{ catData.name }}</p>
                                    </div>

                                    <div class="infofield">
                                        <p>Sugu</p>
                                        <p>{{ catData.sex === "male" ? "isane" : catData.sex === "female" ? "emane" : "teadmata" }}</p>
                                    </div>

                                    <div class="infofield">
                                        <p>Kiibinumber</p>
                                        <p>{{ catData.chip_number ?? "-" }}</p>
                                    </div>

                                    <div class="infofield">
                                        <p>Steriliseeritud</p>
                                        <input
                                            v-if="catData.is_neutered !== null"
                                            disabled
                                            type="checkbox"
                                            :checked="catData.is_neutered"
                                        ></input>
                                        <p v-else>-</p>
                                    </div>

                                    <div class="infofield">
                                        <p>Koloonia</p>
                                        <p>{{ catData.colony?.name ?? "-" }}</p>
                                    </div>

                                    <div class="infofield">
                                        <p>Sunnikuupaev</p>
                                        <p>{{ catData.birth_date?.replaceAll( "-", "." ) ?? "-" }}</p>
                                    </div>

                                    <div class="infofield">
                                        <p>Kas on kodukal?</p>
                                        <input
                                            disabled
                                            type="checkbox"
                                            :checked="false"
                                        ></input>
                                    </div>
                                </div>
                            </div>

                            <!-- care fields -->
                            <div
                                class="flex flex-col gap-2 edit-container"
                                :data-currently-editing="isEditing( 'care' )"
                            >
                                <div class="flex flex-row justify-between items-center">
                                    <h1 class="text-[18px] abril-fatface-regular">Praegune hooldus ja jalgimine</h1>
                                    <Button
                                        class="justify-self-end small"
                                        @click="onClick( 'care' )"
                                    >
                                        {{ formatEditButtonText( "care" ) }}
                                    </Button>
                                </div>

                                <div class="group outfit-400">
                                    <div class="infofield">
                                        <p>Haldur</p>
                                        <p class="capitalize">{{ catData.manager?.display_name || "-" }}</p>
                                    </div>

                                    <div class="infofield">
                                        <p>Hoiukodu</p>
                                        <p>{{ catData.foster_home?.name || "-" }}</p>
                                    </div>

                                    <div class="infofield">
                                        <p>Aadress</p>
                                        <p>{{ catData.foster_home?.address || "-" }}</p>
                                    </div>

                                    <div class="infofield">
                                        <p>Telefoninumber</p>
                                        <p>{{ catData.foster_home?.phone || "-" }}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="col-start-1 2md:col-start-2 xl:row-start-1">
                        <div class="flex flex-col bg-main-bg rounded-[10px] gap-4 px-3 py-3 edit-container">
                            <div
                                class="flex flex-row justify-between"
                                :data-currently-editing="isEditing( 'notes' )"
                            >
                                <h1 class="abril-fatface-regular text-[18px]">Markmed</h1>
                                <Button
                                    class="small"
                                    @click="onClick( 'notes' )"
                                >
                                    {{ formatEditButtonText( "notes" ) }}
                                </Button>
                            </div>

                            <div class="group outfit-400">
                                <p class="text-[14px]">{{ catData.notes || "markmeid pole" }}</p>
                            </div>
                        </div>
                    </div>

                    <div @click.self="showPopUp=false" class="col-start-1 2md:col-span-2 xl:col-start-2 xl:row-start-2 xl:col-span-1">
                        <!-- Pop up for adding medical info -->
                        <div v-if="showPopUp" class="absolute top-80 right-0 w-[40vw] h-[55vh] justify- rounded-lg bg-main-bg p-4 shadow">
                            <div class="flex flex-col gap-6 mb-4">
                                <h1 class="abril-fatface-regular text-[18px]">Lisa kuupäev</h1>
                                <input class="group" type="date" v-model="newMedicalInfo.at_date"/>
                                <h1 class="abril-fatface-regular text-[18px]">Märkmed</h1>
                                <input class="group" type="text" v-model="newMedicalInfo.notes" placeholder="Märkmed" />
                               <div class="flex flex-row gap-6 items-center">
                                <h1 class="abril-fatface-regular text-[18px]">Protseduuri tüüp</h1>
                                    <label class="flex items-center">
                                        <input type="radio" id="vaccine" value="VACCINE" v-model="newMedicalInfo.type"
                                            class="w-4 h-4 accent-[#50192f] mr-2">
                                        Vaktsiin
                                    </label>

                                    <label class="flex items-center">
                                        <input type="radio" id="spot-on" value="SPOT_ON" v-model="newMedicalInfo.type"
                                            class="w-4 h-4 accent-[#50192f] mr-2">
                                        Täpilahus
                                    </label>

                                    <label class="flex items-center">
                                        <input type="radio" id="deworm" value="DEWORMER" v-model="newMedicalInfo.type"
                                            class="w-4 h-4 accent-[#50192f] mr-2">
                                        Ussirohi
                                    </label>
                                    </div>
                                <h1 class="abril-fatface-regular text-[18px]">Lae üles PDF</h1>
                                <input class="group" type="file" @change="(e: Event) => {
                                    const target = e.target as HTMLInputElement;
                                    if (target?.files?.length) {
                                        newMedicalInfo.file = target.files[0];
                                    } else {
                                        newMedicalInfo.file = undefined;
                                    }
                                }" />
                                <h1 class="abril-fatface-regular text-[18px]">Maksumus</h1>
                                <div class="flex flex-row gap-40">
                                    <input class="group w-1/8" type="number" v-model="newMedicalInfo.payment"/>
                                    <Button class="abril-fatface-regular bg-[#E0E0E0] text-[28px]" @click="saveProcedure">Salvesta</Button>
                                </div>
                                </div>
                        <!--  -->
                        </div>
                        
                        <div class="flex flex-col bg-main-bg rounded-[10px] gap-4 px-3 py-3">
                            <div class="flex flex-row justify-between">
                                <h1 class="abril-fatface-regular text-[18px]">Meditsiiniline info</h1>
                                <h1 @click="showPopUp=true" class="abril-fatface-regular text-[24px] cursor-pointer">LISA +</h1>
                            </div>
                            <h1 class="group abril-fatface-regular text-[18px] bg-[#E0E0E0] rounded-[10px]">MAKSUMUS :  {{ totalPayment }}€</h1>
                            <div v-for="(item, index) in medicalInfo" :key="item.id" :class="['flex flex-row border-[1px] border-border-group border-solid px-4 py-2 rounded-[5px] justify-between gap-4 p-2 rounded-lg transition text-sm mb-2', index % 2 === 0 ? 'bg-main-bg' : 'bg-[#EAEAEA]']">
                                <p>{{ item.at_date }}</p>
                                <p>{{ item.type}}</p>
                                <p>{{ item.notes }}</p>
                                <p>{{ item.payment }}€</p>
                                <button class="bg-[#E0E0E0] w-20 rounded-[10px]">Muuda</button>
                            </div>
                        </div>
                    
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import Button from '@/components/atoms/Button.vue';
import BreadCrumbs from '@/components/organisms/BreadCrumbs.vue';
import Status from '@/components/atoms/filter-table/Status.vue';

import { addProcedureCatsCatIdProceduresPost, getCatCatsCatIdGet, listProceduresCatsCatIdProceduresGet } from '@/gen_types/sdk.gen';
import { type CatRead, type ProcedureRead } from '@/gen_types/types.gen';
import { computed, reactive, ref, watch } from 'vue';
import { useRouter } from "vue-router";

const router = useRouter( )

const status_to_readable: { [ key in CatRead[ "status" ] ]: string } = {
  "ACTIVE": "Otsib kodu",
  "FOSTER": "Ajutises kodus",
  "ADOPTED": "Uues kodus",
  "ARCHIVED": "Kiisudemaal",
  "MISSING": "Kadunud",
  "RESERVED": "Broneeritud"
}

const status_to_color: { [ key in CatRead[ "status" ] ]: "green" | "yellow" | "red" | "black" | "gray" } = {
  "ACTIVE": "yellow",
  "FOSTER": "yellow",
  "ADOPTED": "green",
  "ARCHIVED": "black",
  "MISSING": "red",
  "RESERVED": "gray"
}

const showPopUp = ref( false );
const medicalInfo = ref< ProcedureRead[] | null >( null );
const time = ref( "" );
const notes = ref( "" );
const cost = ref( 0 );

const catData = ref< CatRead | null >( null );

type EditableFields = "status" | "main" | "care" | "notes";
type EditSubmit = ( ) => boolean;

const currentlyEditing = ref< EditableFields | null >( null );

const isEditing = ( what: EditableFields ) => currentlyEditing.value === what;
const formatEditButtonText = ( what: EditableFields ) => isEditing( what ) ? "Salvesta" : "Muuda";

const totalPayment = computed( ( ) => {
    if ( medicalInfo.value === null ) return 0;

    let total = 0;
    medicalInfo.value.forEach( item => {
        total += item.payment ?? 0;
    } )

    return total;
} )

const saveField: Record< EditableFields, EditSubmit > = {
    status: ( ) => false,
    main: ( ) => false,
    care: ( ) => false,
    notes: ( ) => false
}

const onClick = ( what: EditableFields ) => {
    if ( currentlyEditing.value === null )
        currentlyEditing.value = what;
    else if ( isEditing( what ) ) {
        if ( !saveField[ what ] ) console.error( `no save callback function for "${ what }" exists, can't save."` );
        else {
            const res = saveField[ what ]( );

            if ( !res ) console.warn( `save callback for "${ what }" failed` );
        }
        currentlyEditing.value = null;
    }
}

const newMedicalInfo = reactive( {
    catId: null as number | null,
    type: "",
    is_repeat: true,
    at_date: "",
    notes: "",
    file: undefined as File | undefined,
    payment: 0
})

const fetchCatInfo = ( id: any ) => {
    getCatCatsCatIdGet({
        path: { cat_id: Number( id ) }
    }).then( res => {
        catData.value = res.data;
        newMedicalInfo.catId = res.data.id;
    })
}

const fetchMedicalInfo = ( id: any ) => {
    listProceduresCatsCatIdProceduresGet({
        path: { cat_id: Number( id ) }
    }).then( res => {
        console.log( res )
        medicalInfo.value = res.data
        console.log( medicalInfo.value )
    })
}



async function saveProcedure() {
  console.log("saveProcedure called")

  console.log("✅ Payload:", {
    cat_id: newMedicalInfo.catId,
    type: newMedicalInfo.type,
    is_repeat: newMedicalInfo.is_repeat,
    at_date: newMedicalInfo.at_date,
    notes: newMedicalInfo.notes,
    payment: newMedicalInfo.payment
  })

  try {
    const res = await addProcedureCatsCatIdProceduresPost({
      path: { cat_id: Number(newMedicalInfo.catId) },
        body: {
            payload: {
            type: newMedicalInfo.type,
            is_repeat: newMedicalInfo.is_repeat,
            at_date: newMedicalInfo.at_date,
            notes: newMedicalInfo.notes,
            file: newMedicalInfo.file ?? null,
            payment: newMedicalInfo.payment
            }
    }
    })
    console.log("Response:", res)
    showPopUp.value = false
    fetchMedicalInfo( router.currentRoute.value.params.id ); // Refresh medical info after adding new procedure
  } catch (error: any) {
    console.error("Error adding procedure:", error)
    if (error.response) {
      console.error("Response data:", error.response.data)
      console.error("Response status:", error.response.status)
      console.error("Response headers:", error.response.headers)
    }
  }
}

watch(
    ( ) => router.currentRoute.value.params.id,
    ( newId ) => fetchCatInfo( newId )
);
fetchCatInfo( router.currentRoute.value.params.id );
fetchMedicalInfo( router.currentRoute.value.params.id );
</script>

<style lang="css" scoped>
.group {
    @apply border-[1px] border-border-group border-solid px-4 py-2 rounded-[5px] flex flex-col gap-2;
}

.infofield {
    @apply flex justify-between text-[#1F1F1F] text-opacity-70 text-[14px];

    & :last-child {
        @apply font-bold text-[#222222] text-opacity-100;
    }
}

.edit-container .group {
    @apply bg-main-bg;
}

#cat-info-container:has( [data-currently-editing=true] ) {
    & .edit-container:not([data-currently-editing=true]) .group {
        filter: brightness( .9 );
        user-select: none;
        cursor: not-allowed;
    }
}
</style>