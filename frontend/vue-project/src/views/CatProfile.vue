<template>
	<div class="flex flex-col bg-cat-bg px-4 py-6 gap-8">
		<div class="relative flex flex-col z-1">
			<div
				class="absolute w-full h-[190px] bg-cat-header rounded-[10px] z-0"
			>
			</div>

			<div class="flex flex-col px-4 pt-12 z-10 gap-2">
				<BreadCrumbs class="light"/>

				<div
					v-if="catData?.id"
					id="cat-info-container"
					class="grid grid-cols-1 w-full 2md:grid-cols-2 xl:grid-rows-[auto_1fr] xl:grid-cols-[2fr_3fr] px-4 gap-5"
				>
					<div class="col-start-1 xl:row-start-1 xl:row-span-2">
						<div class="flex flex-col w-full bg-main-bg rounded-[10px] gap-4 px-3 py-3">
							<div class="flex justify-center items-center">
								<Selection
									:color="status_to_color[ catData.status ]"
									:label="status_to_readable[ catData.status ]"
									:disableEditWithAlt="true"
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
								>

								<h1 class="uppercase text-[18px] abril-fatface-regular">{{ catData.name }}</h1>

								<button class="mr-0 ml-auto small">
									Lae pilt ules
								</button>
							</div>

							<div
								class="flex flex-col gap-2 edit-container"
								:data-editing="editing.main"
							>
								<div class="flex flex-row justify-between items-center">
									<h1 class="text-[18px] abril-fatface-regular">Peamine Info</h1>

									<div
										class="flex gap-2 justify-self-end"
									>
										<button
											v-if="editing.main"
											class="justify-self-end small"
											@click="submitEdit( 'main' )"
										>
											<FiSave :size="EDIT_ICON_SIZE"/>
										</button>

										<button
											v-if="editing.main"
											class="justify-self-end small"
											@click="_ => {
												editing.main = false;
												syncMainEditFieldsToCatData( catData );
											}"
										>
											<FiX :size="EDIT_ICON_SIZE"/>
										</button>

										<button
											v-if="!editing.main"
											class="justify-self-end small svg-fill"
											@click="editing.main = true"
										>
											<TfiPencil :size="EDIT_ICON_SIZE"/>
										</button>
									</div>
								</div>

								<!-- main data fields -->
								<div class="group outfit-400">
									<div class="infofield">
										<p>Nimi</p>

										<InputField pattern="[a-zA-Z](([a-zA-Z]|\s)*)" placeholder="Kassi nimi" class="placeholder-shown:border-red-600" :text="catData.name" v-model="mainEditFields.name" :isEditing="editing.main"/>
									</div>

									<div class="infofield">
										<p>Sugu</p>

										<SelectField
											:defaultSelected="catData.sex ? mainEditFieldOptions.sex.indexOf( catData.sex ) : mainEditFieldOptions.sex.indexOf( 'unknown' )"
											:options="mainEditFieldOptions.sex
												.map( ( s, i ) => ({ name: s, idx: i }) )
												.reduce( ( acc, c ) => ({ ...acc, [ c.idx ]: c.name }), { })"
											v-model="mainEditFields.sex_idx"
											:isEditing="editing.main"
										/>
									</div>

									<div class="infofield">
										<p>Kiibinumber</p>
										<InputField
											pattern="[0-9]{0}|[0-9]{15}"
											maxlength="15"
											:text="catData.chip_number || '-'" v-model="mainEditFields.chip_number"
											:isEditing="editing.main"
										/>
									</div>

									<div class="infofield">
										<p>Steriliseeritud</p>

										<CheckboxField
											:defaultChecked="!!catData.is_neutered"
											v-model="mainEditFields.sterilized"
											:isEditing="editing.main"
										/>
									</div>

									<div class="infofield">
										<p>Koloonia</p>

										<SelectField
											:defaultSelected="catData?.colony?.id || -1"
											:options="{
												[ -1 ]: '-',
												...(
													mainEditFieldOptions.colony
														.map( c => ({ name: c.name, id: c.id }) )
														.reduce( ( acc, v ) => ({ ...acc, [ v.id ]: v.name }), { } )
												)
											}"
											v-model="mainEditFields.colony_id"
											:isEditing="editing.main"
										/>
									</div>

									<div class="infofield">
										<p>Sunnikuupaev</p>

										<InputField
											type="date"
											:text="catData.birth_date || '-'"
											:isEditing="editing.main"
											v-model="mainEditFields.birth_date"
										/>

									</div>

									<div class="infofield">
										<p>Kas on kodukal?</p>

										<CheckboxField
											:defaultChecked="false"
											v-model="mainEditFields.on_homepage"
											:isEditing="editing.main"
										/>
									</div>
								</div>
							</div>

							<!-- care fields -->
							<div
								class="flex flex-col gap-2 edit-container"
								:data-editing="editing.care"
							>
								<div class="flex flex-row justify-between items-center">
									<h1 class="text-[18px] abril-fatface-regular">Praegune hooldus ja jalgimine</h1>

									<div
										class="flex gap-2 justify-self-end"
									>
										<button
											v-if="editing.care"
											class="justify-self-end small"
											@click="submitEdit( 'care' )"
										>
											<FiSave :size="EDIT_ICON_SIZE"/>
										</button>

										<button
											v-if="editing.care"
											class="justify-self-end small"
											@click="_ => {
												editing.care = false
												syncCatManagementFieldsToCatData( catData );
											}"
										>
											<FiX :size="EDIT_ICON_SIZE"/>
										</button>

										<button
											v-if="!editing.care"
											class="justify-self-end small svg-fill"
											@click="editing.care = true"
										>
											<TfiPencil :size="EDIT_ICON_SIZE"/>
										</button>
									</div>
								</div>

								<div class="group outfit-400">
									<div class="infofield">
										<p>Haldur</p>

										<SelectField
											:defaultSelected="catData.manager.id || MANAGER_CASES.NONE"
											:options="{
												[ -1 ]: '-',
												...(
													catManagementFieldOptions.managers
														.map( c => ({ name: c.display_name, id: c.id }) )
														.reduce( ( acc, v ) => ({ ...acc, [ v.id ]: v.name }), { } )
												)
											}"
											v-model="currentCatManagementFields.manager_id"
											:isEditing="editing.care"
										/>
									</div>

									<div class="infofield">
										<p>Hoiukodu</p>

										<SelectField
											:defaultSelected="catData.foster_home.id || FOSTER_HOME_CASES.NONE"
											:options="{
												[ -1 ]: '-',
												...(
													catManagementFieldOptions.foster_homes
														.map( c => ({ name: c.name, id: c.id }) )
														.reduce( ( acc, v ) => ({ ...acc, [ v.id ]: v.name }), { } )
												)
											}"
											v-model="currentCatManagementFields.foster_home_id"
											:isEditing="editing.care"
										/>
									</div>

									<div class="infofield">
										<p>Aadress</p>

										<InputField
											:text="catData.foster_home?.address || '-'"
											v-model="currentCatManagementFields.foster_home_address"
											:isEditing="editing.care"
										/>
									</div>

									<div class="infofield">
										<p>Telefoninumber</p>

										<InputField
											:text="catData.foster_home?.phone || '-'"
											v-model="currentCatManagementFields.foster_home_phone_nr"
											:isEditing="editing.care"
										/>
									</div>
								</div>
							</div>
						</div>
					</div>

					<div class="col-start-1 2md:col-start-2 xl:row-start-1">
						<div
							class="flex flex-col bg-main-bg rounded-[10px] gap-4 px-3 py-3 edit-container"
							:data-editing="editing.notes"
						>
							<div
								class="flex flex-row justify-between"
							>
								<h1 class="abril-fatface-regular text-[18px]">Markmed</h1>

								<div
									class="flex gap-2 justify-self-end"
								>
									<button
										v-if="editing.notes"
										class="justify-self-end small"
										@click="submitEdit( 'notes' )"
									>
										<FiSave :size="EDIT_ICON_SIZE"/>
									</button>

									<button
										v-if="editing.notes"
										class="justify-self-end small"
										@click="_ => {
											editing.notes = false;
											syncCatNotesFieldsToCatData( catData );
										}"
									>
										<FiX :size="EDIT_ICON_SIZE"/>
									</button>

									<button
										v-if="!editing.notes"
										class="justify-self-end small svg-fill"
										@click="editing.notes = true"
									>
										<TfiPencil :size="EDIT_ICON_SIZE"/>
									</button>
								</div>
							</div>

							<div class="group outfit-400">
								<TextField
									:text="catData.notes || 'markmeid pole'"
									v-model="catNotes"
									:isEditing="editing.notes"
								/>
							</div>
						</div>
					</div>

					<div class="col-start-1 2md:col-span-2 xl:col-start-2 xl:row-start-2 xl:col-span-1">
						<div class="flex flex-col bg-main-bg rounded-[10px] gap-4 px-3 py-3">
							<div class="flex flex-row justify-between">
								<h1 class="abril-fatface-regular text-[18px]">Meditsiiniline info</h1>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import BreadCrumbs from '@/components/organisms/BreadCrumbs.vue';
import Selection from '@/components/atoms/filter-table/Selection.vue';

import api from "@/api_fetch.ts"
import {
	type CatRead,
	type ColonyRead,
	type FosterHomeRead, type UserRead
} from '@/gen_types/types.gen';
import { ref, watch } from 'vue';
import { useRouter } from "vue-router";
import { useToast } from "primevue";
import { setBreadcrumb } from "@/router/helpers.ts";

import { FiSave, FiX } from "vue-icons-plus/fi";
import { TfiPencil } from "vue-icons-plus/tfi";
import InputField from "@/components/atoms/profile-edit-fields/InputField.vue";
import SelectField from "@/components/atoms/profile-edit-fields/SelectField.vue";
import CheckboxField from "@/components/atoms/profile-edit-fields/CheckboxField.vue";
import TextField from "@/components/atoms/profile-edit-fields/TextField.vue";

const router = useRouter();
const toast = useToast();

const EDIT_ICON_SIZE = 20;

const status_to_readable: { [key in CatRead[ "status" ]]: string } = {
	"ACTIVE": "Otsib kodu",
	"FOSTER": "Ajutises kodus",
	"ADOPTED": "Uues kodus",
	"ARCHIVED": "Kiisudemaal",
	"MISSING": "Kadunud",
	"RESERVED": "Broneeritud"
}

const status_to_color: { [key in CatRead[ "status" ]]: "green" | "yellow" | "red" | "black" | "gray" } = {
	"ACTIVE": "yellow",
	"FOSTER": "yellow",
	"ADOPTED": "green",
	"ARCHIVED": "black",
	"MISSING": "red",
	"RESERVED": "gray"
}

enum COLONY_CASES {
	NONE = -1
}

enum MANAGER_CASES {
	NONE = -1
}

enum FOSTER_HOME_CASES {
	NONE = -1
}

const catData = ref<CatRead | null>( null );

type EditableFields = "status" | "main" | "care" | "notes";
type EditSubmit = () => boolean;

const editing = ref<{ [key in EditableFields]: boolean }>( {
	main: false,
	status: false,
	notes: false,
	care: false,
} );


const mainEditFieldOptions = ref<{
	sex: CatRead[ "sex" ][ ],
	colony: ColonyRead[ ]
}>({
	sex: [ "unknown", "male", "female" ],
	colony: [ ]
});

const catManagementFieldOptions = ref<{
	managers: UserRead[ ],
	foster_homes: FosterHomeRead[ ]
}>({
	managers: [ ],
	foster_homes: [ ]
});

const catNotes = ref< string >( "" );

// ive genuinely went over this in 3 different ways
// staying on this variant of handling data as of now
const mainEditFields = ref<{
	name: string, sex_idx: number, chip_number: string,
	sterilized: boolean, colony_id: number | COLONY_CASES,
	birth_date: string, on_homepage: boolean
}>({
	name: "",
	sex_idx: mainEditFieldOptions.value.sex.indexOf( "unknown" ),
	chip_number: "",
	sterilized: false,
	colony_id: COLONY_CASES.NONE,
	birth_date: "",
	on_homepage: false
});

const currentCatManagementFields = ref<{
	manager_id: number | MANAGER_CASES,
	foster_home_id: number | FOSTER_HOME_CASES,
	foster_home_address: string,
	foster_home_phone_nr: string
}>({
	manager_id: MANAGER_CASES.NONE,
	foster_home_id: FOSTER_HOME_CASES.NONE,
	foster_home_address: "",
	foster_home_phone_nr: ""
});

const syncMainEditFieldsToCatData = ( cat: CatRead ) => {
	mainEditFields.value.name = cat.name // Sten
	mainEditFields.value.sex_idx = mainEditFieldOptions.value.sex.indexOf( cat.sex ?? "unknown" ) // male
	mainEditFields.value.chip_number = cat.chip_number ?? "" //
	mainEditFields.value.sterilized = cat.is_neutered ?? false //
	mainEditFields.value.colony_id = cat.colony ? cat.colony.id : COLONY_CASES.NONE // [object Object]
	mainEditFields.value.birth_date = cat.birth_date ?? "" // 2025-11-04
}

const syncCatManagementFieldsToCatData = ( cat: CatRead ) => {
	currentCatManagementFields.value.manager_id = cat.manager ? cat.manager.id : MANAGER_CASES.NONE;
	currentCatManagementFields.value.foster_home_id = cat.foster_home ? cat.foster_home.id : FOSTER_HOME_CASES.NONE;
	currentCatManagementFields.value.foster_home_address = cat.foster_home?.address || "";
	currentCatManagementFields.value.foster_home_phone_nr = cat.foster_home?.phone || "";
}

const syncCatNotesFieldsToCatData = ( cat: CatRead ) => {
	catNotes.value = cat.notes || "";
}


// set up all fields for selecting
api.getAllColoniesColoniesGet( ).then( res => {
	if ( !res.data ) {
		toast.add({
			severity: "error",
			summary: "Kolooniate laadimine ebaonnestus.",
			life: 3000
		});
		return;
	}

	mainEditFieldOptions.value.colony = res.data;
})
api.listManagersManagersGet( ).then( res => {
	if ( !res.data ) {
		toast.add({
			severity: "error",
			summary: "Vabatahtlike laadimine ebaonnestus.",
			life: 3000
		});
		return;
	}

	catManagementFieldOptions.value.managers = res.data;
})
api.listFosterHomesFosterHomesGet( ).then( res => {
	if ( !res.data ) {
		toast.add({
			severity: "error",
			summary: "Hoiukodude laadimine ebaonnestus.",
			life: 3000
		});
		return;
	}

	catManagementFieldOptions.value.foster_homes = res.data;
})


const saveField: Record<EditableFields, EditSubmit> = {
	status: () => false,
	main: () => false,
	care: () => false,
	notes: () => false
}


const syncCatToSentField: Record<EditableFields, EditSubmit> = {
	status: () => false,
	main: () => false,
	care: () => false,
	notes: () => false
}

const submitEdit = ( what: EditableFields ) => {
	if ( editing.value[ what ] ) {
		if ( !saveField[ what ] ) console.warn( `no save callback function for "${ what }" exists, can't save."` );
		else {
			const res = saveField[ what ]();

			if ( !res ) console.error( `save callback for "${ what }" failed` );
			else {
				if ( !syncCatToSentField[ what ] ) console.warn( `no save callback function for "${ what }" exists, can't save."` );
			}
		}

		editing.value[ what ] = false;
	}
}

const fetchCatInfo = ( id: any ) => {
	api.getCatCatsCatIdGet( {
		path: { cat_id: Number( id ) }
	} ).then( res => {
		if ( !res.data ) {
			toast.add( {
				severity: "error",
				summary: "Kassi laadimine ebaonnestus",
				life: 3000
			} )
			return
		}

		catData.value = res.data;

		syncMainEditFieldsToCatData( res.data );
		syncCatManagementFieldsToCatData( res.data );
		syncCatNotesFieldsToCatData( res.data );

		// bug: redirects break with this (on logout no redirect)
		// HAVE to set directly, modifying meta won't update breadcrumbs (good 2h spent)
		router.currentRoute.value = {
			...router.currentRoute.value,
			meta: {
				breadcrumbs: setBreadcrumb( router.currentRoute.value.meta, -1, `${ res.data.name } profiil` ),
				sidebar: true
			}
		}
	} )
}

watch(
	() => router.currentRoute.value.params.id,
	( newId ) => fetchCatInfo( newId )
);

fetchCatInfo( router.currentRoute.value.params.id );
</script>

<style lang="css" scoped>
.group {
	@apply border-[1px] border-border-group border-solid px-4 py-2 rounded-[5px] flex flex-col gap-2;
}

.infofield {
	@apply flex justify-between text-[#1F1F1F] text-opacity-70 text-[14px] items-center;

	& :last-child {
		@apply font-bold text-[#222222] text-opacity-100;
	}
}

.edit-container .group {
	@apply bg-main-bg;
}

.edit-container[data-editing=true] .group {
	gap: 4px;
	padding: 0.375rem 0.5rem 0.375rem 1rem;
}


button {
	& * {
		@apply stroke-[#888] transition-colors;
	}

	&:hover * {
		@apply stroke-[#444];
	}
}

button.svg-fill {
	& * {
		@apply fill-[#888] transition-colors;
	}

	&:hover * {
		@apply fill-[#444];
	}
}
</style>