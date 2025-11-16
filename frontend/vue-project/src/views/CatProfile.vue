<template>
	<div class="flex flex-col bg-cat-bg px-4 py-6 gap-8">
		<div class="relative flex flex-col z-1">
			<div
				class="absolute w-full h-[190px] bg-cat-header rounded-[10px] z-0"
			>
			</div>

			<div class="flex flex-col px-4 pt-12 z-10 gap-2">
				<BreadCrumbs
					class="light"
					:slugs="{ name: catData?.name || 'Kassi' }"
				/>

				<div
					v-if="catData?.id"
					id="cat-info-container"
					class="grid grid-cols-1 w-full 2md:grid-cols-2 xl:grid-rows-[auto_1fr] xl:grid-cols-[2fr_3fr] px-4 gap-5"
				>
					<div class="col-start-1 xl:row-start-1 xl:row-span-2">
						<div class="flex flex-col w-full bg-main-bg rounded-[10px] gap-4 px-3 py-3">
							<form
								class="flex justify-center items-center gap-2"
								@submit.prevent="submitEdit( 'status' )"
							>
								<Selection
									:color="status_to_color[ catData.status ]"
									:disableEditWithAlt="true"
								/>

								<SelectField
									:defaultSelected="selectableStatuses[ catData.status ]"
									:options="selectableStatusesIndex"
									v-model="catStatusIndex"
									:isEditing="editing.status === EditingStatus.EDITING || editing.status === EditingStatus.SUBMITTING"
									:disabled="editing.status === EditingStatus.SUBMITTING"
									@update:modelValue="submitEdit( 'status' )"
								/>

								<button
									v-if="editing.status === EditingStatus.SUBMITTING"
									class="justify-self-end small"
									type="submit"
								>
									<CgSpinner
										:size="EDIT_ICON_SIZE"
										class="animate-spin"
									/>
								</button>

								<button
									v-if="editing.status !== EditingStatus.IDLE"
									class="justify-self-end small"
									@click="_ => {
										editing.status = EditingStatus.IDLE;

										if ( catData ) syncCatStatusToCatData( catData );
									}"
								>
									<FiX :size="EDIT_ICON_SIZE"/>
								</button>

								<button
									v-if="editing.status === EditingStatus.IDLE"
									class="justify-self-end small svg-fill"
									@click="editing.status = EditingStatus.EDITING"
								>
									<TfiPencil :size="EDIT_ICON_SIZE"/>
								</button>
							</form>

							<!-- cat heading info -->
							<div
								class="flex flex-row items-center gap-5"
							>
								<div
									class="w-[72px] h-[72px] rounded-full"
								>
									<img
										v-if="catData.primary_photo_object"
										class="w-[72px] h-[72px] rounded-full"
										src=""
										alt=""
										ref="catPfpImgRef"
									/>

									<div
										v-else
										class="w-[72px] h-[72px] bg-gray-200 rounded-full"
									>

									</div>
								</div>

								<h1 class="uppercase text-[18px] abril-fatface-regular">{{ catData.name }}</h1>

								<ImageUploadButton
									v-model="catProfilePicture"
									class="mr-0 ml-auto small"
								/>
							</div>

							<form
								class="flex flex-col gap-2 edit-container"
								:data-editing="editing.main !== EditingStatus.IDLE"
								@submit.prevent="submitEdit( 'main' )"
							>
								<div class="flex flex-row justify-between items-center">
									<h1 class="text-[18px] abril-fatface-regular">Peamine Info</h1>

									<div
										class="flex gap-2 justify-self-end"
									>
										<button
											v-if="editing.main !== EditingStatus.IDLE"
											class="justify-self-end small"
											type="submit"
										>
											<FiSave
												v-if="editing.main === EditingStatus.EDITING"
												:size="EDIT_ICON_SIZE"
											/>

											<CgSpinner
												v-else
												:size="EDIT_ICON_SIZE"
												class="animate-spin"
											/>
										</button>

										<button
											v-if="editing.main !== EditingStatus.IDLE"
											class="justify-self-end small"
											@click="_ => {
												editing.main = EditingStatus.IDLE;

												if ( catData )
													syncMainEditFieldsToCatData( catData );
											}"
										>
											<FiX :size="EDIT_ICON_SIZE"/>
										</button>

										<button
											v-if="editing.main === EditingStatus.IDLE"
											class="justify-self-end small svg-fill"
											@click="editing.main = EditingStatus.EDITING"
										>
											<TfiPencil :size="EDIT_ICON_SIZE"/>
										</button>
									</div>
								</div>

								<!-- main data fields -->
								<div class="group outfit-400">
									<div class="infofield">
										<p>Nimi</p>

										<InputField
											pattern="[a-zA-Z](([a-zA-Z]|\s)*)"
											minlength="1"
											placeholder="Kassi nimi"
											class="placeholder-shown:border-red-600"
											:text="catData.name"
											required
											v-model="mainEditFields.name"
											:isEditing="[ EditingStatus.EDITING, EditingStatus.SUBMITTING ].includes( editing.main )"
											:disabled="EditingStatus.SUBMITTING === editing.main"
										/>
									</div>

									<div class="infofield">
										<p>Sugu</p>

										<SelectField
											:defaultSelected="catData.sex ? mainEditFieldOptions.sex.indexOf( catData.sex ) : mainEditFieldOptions.sex.indexOf( 'unknown' )"
											:options="mainEditFieldOptions.sex
												.map( ( s, i ) => ({ name: s, idx: i }) )
												.reduce( ( acc, c ) => ({ ...acc, [ c.idx ]: c.name }), { })"
											v-model="mainEditFields.sex_idx"
											:isEditing="[ EditingStatus.EDITING, EditingStatus.SUBMITTING ].includes( editing.main )"
											:disabled="EditingStatus.SUBMITTING === editing.main"
										/>
									</div>

									<div class="infofield">
										<p>Kiibinumber</p>
										<InputField
											pattern="[0-9]{0}|[0-9]{15}"
											maxlength="15"
											:text="catData.chip_number || '-'" v-model="mainEditFields.chip_number"
											:isEditing="[ EditingStatus.EDITING, EditingStatus.SUBMITTING ].includes( editing.main )"
											:disabled="EditingStatus.SUBMITTING === editing.main"
										/>
									</div>

									<div class="infofield">
										<p>Steriliseeritud</p>

										<CheckboxField
											:defaultChecked="!!catData.is_neutered"
											v-model="mainEditFields.sterilized"
											:isEditing="[ EditingStatus.EDITING, EditingStatus.SUBMITTING ].includes( editing.main )"
											:disabled="EditingStatus.SUBMITTING === editing.main"
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
											:isEditing="[ EditingStatus.EDITING, EditingStatus.SUBMITTING ].includes( editing.main )"
											:disabled="EditingStatus.SUBMITTING === editing.main"
										/>
									</div>

									<div class="infofield">
										<p>Sunnikuupaev</p>

										<InputField
											type="date"
											:text="catData.birth_date || '-'"
											v-model="mainEditFields.birth_date"
											:isEditing="[ EditingStatus.EDITING, EditingStatus.SUBMITTING ].includes( editing.main )"
											:disabled="EditingStatus.SUBMITTING === editing.main"
										/>

									</div>

									<div class="infofield">
										<p>Kas on kodukal?</p>

										<CheckboxField
											:defaultChecked="false"
											v-model="mainEditFields.on_homepage"
											:isEditing="[ EditingStatus.EDITING, EditingStatus.SUBMITTING ].includes( editing.main )"
											:disabled="EditingStatus.SUBMITTING === editing.main"
										/>
									</div>
								</div>
							</form>

							<!-- care fields -->
							<form
								class="flex flex-col gap-2 edit-container"
								:data-editing="editing.care !== EditingStatus.IDLE"
								@submit.prevent="submitEdit( 'care' )"
							>
								<div class="flex flex-row justify-between items-center">
									<h1 class="text-[18px] abril-fatface-regular">Praegune hooldus ja jalgimine</h1>

									<div
										class="flex gap-2 justify-self-end"
									>
										<button
											v-if="editing.care !== EditingStatus.IDLE"
											class="justify-self-end small"
											type="submit"
										>
											<FiSave
												v-if="editing.care === EditingStatus.EDITING"
												:size="EDIT_ICON_SIZE"
											/>

											<CgSpinner
												v-else
												:size="EDIT_ICON_SIZE"
												class="animate-spin"
											/>
										</button>

										<button
											v-if="editing.care !== EditingStatus.IDLE"
											class="justify-self-end small"
											@click="_ => {
												editing.care = EditingStatus.IDLE;

												if ( catData )
													syncCatManagementFieldsToCatData( catData );
											}"
										>
											<FiX :size="EDIT_ICON_SIZE"/>
										</button>

										<button
											v-if="editing.care === EditingStatus.IDLE"
											class="justify-self-end small svg-fill"
											@click="editing.care = EditingStatus.EDITING"
										>
											<TfiPencil :size="EDIT_ICON_SIZE"/>
										</button>
									</div>
								</div>

								<div class="group outfit-400">
									<div class="infofield">
										<p>Haldur</p>

										<SelectField
											:defaultSelected="catData?.manager?.id || MANAGER_CASES.NONE"
											:options="{
												[ -1 ]: '-',
												...(
													catManagementFieldOptions.managers
														.map( c => ({ name: c.display_name, id: c.id }) )
														.reduce( ( acc, v ) => ({ ...acc, [ v.id ]: v.name }), { } )
												)
											}"
											v-model="currentCatManagementFields.manager_id"
											:isEditing="[ EditingStatus.EDITING, EditingStatus.SUBMITTING ].includes( editing.care )"
											:disabled="EditingStatus.SUBMITTING === editing.care"
										/>
									</div>

									<div class="infofield">
										<p>Hoiukodu</p>

										<SelectField
											:defaultSelected="catData?.foster_home?.id || FOSTER_HOME_CASES.NONE"
											:options="{
												[ -1 ]: '-',
												...(
													catManagementFieldOptions.foster_homes
														.map( c => ({ name: c.name, id: c.id }) )
														.reduce( ( acc, v ) => ({ ...acc, [ v.id ]: v.name }), { } )
												)
											}"
											v-model="currentCatManagementFields.foster_home_id"
											:isEditing="[ EditingStatus.EDITING, EditingStatus.SUBMITTING ].includes( editing.care )"
											:disabled="EditingStatus.SUBMITTING === editing.care"
										/>
									</div>

									<div class="infofield">
										<p>Aadress</p>

										<InputField
											:text="catData.foster_home?.address || '-'"
											v-model="currentCatManagementFields.foster_home_address"
											:isEditing="[ EditingStatus.EDITING, EditingStatus.SUBMITTING ].includes( editing.care )"
											:disabled="EditingStatus.SUBMITTING === editing.care || currentCatManagementFields.foster_home_id === FOSTER_HOME_CASES.NONE"
										/>
									</div>

									<div class="infofield">
										<p>Telefoninumber</p>

										<InputField
											:text="catData.foster_home?.phone || '-'"
											v-model="currentCatManagementFields.foster_home_phone_nr"
											:isEditing="[ EditingStatus.EDITING, EditingStatus.SUBMITTING ].includes( editing.care )"
											:disabled="EditingStatus.SUBMITTING === editing.care || currentCatManagementFields.foster_home_id === FOSTER_HOME_CASES.NONE"
										/>
									</div>
								</div>
							</form>
						</div>
					</div>

					<div class="col-start-1 2md:col-start-2 xl:row-start-1">
						<div
							class="flex flex-col bg-main-bg rounded-[10px] gap-4 px-3 py-3 edit-container"
							:data-editing="editing.notes !== EditingStatus.IDLE"
						>
							<div
								class="flex flex-row justify-between"
							>
								<h1 class="abril-fatface-regular text-[18px]">Markmed</h1>

								<div
									class="flex gap-2 justify-self-end"
								>
									<button
										v-if="editing.notes !== EditingStatus.IDLE"
										class="justify-self-end small"
										@click="submitEdit( 'notes' )"
									>
										<FiSave
											v-if="editing.notes === EditingStatus.EDITING"
											:size="EDIT_ICON_SIZE"
										/>

										<CgSpinner
											v-else
											:size="EDIT_ICON_SIZE"
											class="animate-spin"
										/>
									</button>

									<button
										v-if="editing.notes !== EditingStatus.IDLE"
										class="justify-self-end small"
										@click="_ => {
											editing.notes = EditingStatus.IDLE;

											if ( catData )
												syncCatNotesFieldsToCatData( catData );
										}"
									>
										<FiX :size="EDIT_ICON_SIZE"/>
									</button>

									<button
										v-if="editing.notes === EditingStatus.IDLE"
										class="justify-self-end small svg-fill"
										@click="editing.notes = EditingStatus.EDITING"
									>
										<TfiPencil :size="EDIT_ICON_SIZE"/>
									</button>
								</div>
							</div>

							<div class="group outfit-400">
								<TextField
									:text="catData.notes || 'markmeid pole'"
									v-model="catNotes"
									:isEditing="[ EditingStatus.EDITING, EditingStatus.SUBMITTING ].includes( editing.notes )"
									:disabled="EditingStatus.SUBMITTING == editing.notes"
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
	type CatRead, type CatUpdate,
	type ColonyRead,
	type FosterHomeRead, type UserRead
} from '@/gen_types/types.gen';
import { ref, watch } from 'vue';
import { useRouter } from "vue-router";
import { useToast } from "primevue";

import { CgSpinner } from "vue-icons-plus/cg";
import { FiSave, FiX } from "vue-icons-plus/fi";
import { TfiPencil } from "vue-icons-plus/tfi";
import InputField from "@/components/atoms/profile-edit-fields/InputField.vue";
import SelectField from "@/components/atoms/profile-edit-fields/SelectField.vue";
import CheckboxField from "@/components/atoms/profile-edit-fields/CheckboxField.vue";
import TextField from "@/components/atoms/profile-edit-fields/TextField.vue";
import ImageUploadButton from "@/components/atoms/profile-edit-fields/ImageUploadButton.vue";

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

// SelectField expects { index: name } dict
// map each status key to an index ({ name: index }), easier to look up with cat status
const selectableStatuses =
	Object.entries( status_to_readable )
	.map( ([ key, value ], index ) => ({ index, name: key }) )
	.reduce( ( acc, curr ) => ({ ...acc, [ curr.name ]: curr.index }), { } ) as { [ key in CatRead[ "status" ] ]: number };
// for SelectField we need a ""reverse"" table of above
const selectableStatusesIndex: { [ key: number ]: ( typeof status_to_readable )[ keyof typeof status_to_readable ] } =
	Object.entries( selectableStatuses )
		// losing strictness for a sec
		.map( ([ key, value ]: [ string, number ]) => ({ key, value }) )
		// @ts-ignore
		.reduce( ( acc, curr: { key: CatRead[ "status" ], value: number } ) => ({ ...acc, [ curr.value ]: status_to_readable[ curr.key ] }), { } );

// special cases for selecting "null" entries for
// colonies, managers and foster homes
// enums are made just to make readability better
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
const catPfpImgRef = ref< HTMLImageElement | null >( null );

type EditableFields = "pfp" | "status" | "main" | "care" | "notes";
type EditSubmit = () => Promise< boolean >;
enum EditingStatus {
	EDITING = 0,
	SUBMITTING = 1,
	IDLE = 2
}

const editing = ref<{ [key in EditableFields]: EditingStatus }>( {
	pfp: 	EditingStatus.IDLE,
	main:	EditingStatus.IDLE,
	status: EditingStatus.IDLE,
	notes:  EditingStatus.IDLE,
	care:   EditingStatus.IDLE,
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


// ive genuinely went over this in 3 different ways
// staying on this variant of handling data as of now
const catStatusIndex = ref< number >( 0 );
const catProfilePicture = ref< null | File >( null );

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

const catNotes = ref< string >( "" );

// syncing editable data to cats, called on cat load
const syncCatStatusToCatData = ( cat: CatRead ) => {
	catStatusIndex.value = selectableStatuses[ cat.status ];
}
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


const updateCatProfileImage = async ( ) => {
	if ( !catData.value?.primary_photo_object || !catPfpImgRef.value ) return;

	const res = await api.getImageImageObjectNameGet({
		path: {
			object_name: catData.value.primary_photo_object
		}
	});

	if ( !res.data ) {
		toast.add( {
			severity: "error",
			summary: "Kassi pildi laadimine ebaonnestus",
			life: 3000
		} );
		return;
	}

	const blob = res.data as Blob;
	catPfpImgRef.value.src = URL.createObjectURL( blob );
}

// when foster home selection changes we also have to update its corresponding
// fields in the form, address & phonenr atm
watch(
	( ) => currentCatManagementFields.value.foster_home_id,
	( newFosterHomeId ) => {
		// no foster home selected, clear address and phonenr
		if ( newFosterHomeId === FOSTER_HOME_CASES.NONE ) {
			currentCatManagementFields.value.foster_home_phone_nr = "";
			currentCatManagementFields.value.foster_home_address = "";
			return;
		}

		if (catManagementFieldOptions.value.foster_homes.length === 0) {
			console.warn( `Foster home id changed but we don't have any fetched foster homes` );
			return;
		}

		const fosterHome = catManagementFieldOptions.value.foster_homes.find( fh => fh.id === newFosterHomeId );

		if ( !fosterHome ) {
			toast.add({
				severity: "error",
				life: 3000,
				summary: "Hoiukodu detailide laadminie ebaonnestus."
			});
			return;
		}

		currentCatManagementFields.value.foster_home_phone_nr = fosterHome.phone || "";
		currentCatManagementFields.value.foster_home_address = fosterHome.address || "";
	}
)

// save field callbacks
// each is used when their corresponding group gets saved
const saveField: Record<EditableFields, EditSubmit> = {
	status: async ( ) => {
		if ( !catData.value ) {
			toast.add({
				severity: "warn",
				summary: "Kassi pole.",
				life: 3000
			});
			return false;
		}

		const readableStatusName = selectableStatusesIndex[ catStatusIndex.value ];

		if ( !readableStatusName ) {
			console.error( `couldn't find readable status for index ${ catStatusIndex.value } in ${ selectableStatusesIndex }` );
			return false;
		}

		const backendStatusName = Object.entries( status_to_readable ).map( ([ dbName, prettyName ]) => ({ dbName, prettyName }) ).find( t => t.prettyName === readableStatusName );

		if ( !backendStatusName ) {
			console.error( `couldn't find backend status name for ${ readableStatusName } in ${ status_to_readable }` );
			return false;
		}

		const res = await api.updateCatCatsCatIdPatch({
			body: {
				payload: JSON.stringify({
					status: backendStatusName.dbName
				} as CatUpdate )
			},
			path: {
				cat_id: catData.value.id
			}
		});

		if ( !res.data ) {
			toast.add({
				severity: "error",
				summary: "Kassi staatuse uuendamine ebaonnestus.",
				life: 3000
			});

			return false;
		}

		catData.value = res.data;

		return true;
	},
	pfp: async ( ) => {
		if ( !catData.value ) {
			toast.add({
				severity: "warn",
				summary: "Kassi pole.",
				life: 3000
			});
			return false;
		}

		if ( !catProfilePicture.value ) {
			toast.add({
				severity: "warn",
				summary: "Kassi pilti pole.",
				life: 3000
			});
			return false;
		}

		const res = await api.updateCatCatsCatIdPatch({
			body: {
				primary_image: catProfilePicture.value,
				payload: JSON.stringify({ })
			},
			path: {
				cat_id: catData.value.id
			}
		});

		if ( !res.data ) {
			toast.add({
				severity: "error",
				summary: "Kassi pildi uuendamine ebaonnestus.",
				life: 3000
			});

			return false;
		}

		catData.value = res.data;

		if ( catPfpImgRef.value ) {
			catPfpImgRef.value.src = URL.createObjectURL( catProfilePicture.value );
		}

		return true;
	},
	main: async ( ) => {
		if ( !catData.value ) {
			toast.add({
				severity: "warn",
				summary: "Kassi pole.",
				life: 3000
			});
			return false;
		}

		const res = await api.updateCatCatsCatIdPatch({
			body: {
				payload: JSON.stringify({
					name: mainEditFields.value.name,
					sex: mainEditFieldOptions.value.sex[ mainEditFields.value.sex_idx ],
					chip_number: mainEditFields.value.chip_number,
					is_neutered: mainEditFields.value.sterilized,
					colony_id: mainEditFields.value.colony_id === COLONY_CASES.NONE ? null : mainEditFields.value.colony_id,
					birth_date: mainEditFields.value.birth_date,
					// on_homepage: mainEditFields.value.on_homepage
				} as CatUpdate )
			},
			path: {
				cat_id: catData.value.id
			}
		});

		if ( !res.data ) {
			toast.add({
				severity: "error",
				summary: "Kassi uuendamine ebaonnestus",
				life: 3000
			});

			return false;
		}

		catData.value = res.data;

		return true;
	},
	care: async ( ) => {
		if ( !catData.value ) {
			toast.add({
				severity: "warn",
				summary: "Kassi pole.",
				life: 3000
			});
			return false;
		}

		// we can have a cat edit and foster home edit at the same time
		const [ catEditRes, fosterHomeEditRes ] = await Promise.all([
			api.updateCatCatsCatIdPatch({
				body: {
					payload: JSON.stringify({
						manager_id: currentCatManagementFields.value.manager_id === MANAGER_CASES.NONE ? null : currentCatManagementFields.value.manager_id,
						foster_home_id: currentCatManagementFields.value.foster_home_id === FOSTER_HOME_CASES.NONE ? null : currentCatManagementFields.value.foster_home_id
					} )
				},
				path: {
					cat_id: catData.value.id
				}
			}),

			// can only update foster home when we have one selected
			currentCatManagementFields.value.foster_home_id !== FOSTER_HOME_CASES.NONE && api.updateCatFosterHomesHomeIdPatch({
				body: {
					phone: currentCatManagementFields.value.foster_home_phone_nr,
					address: currentCatManagementFields.value.foster_home_address
				},
				path: {
					home_id: currentCatManagementFields.value.foster_home_id
				}
			})
		]);

		let failedAny = false;

		if ( !catEditRes.data ) {
			toast.add({
				severity: "error",
				summary: "Kassi uuendamine ebaonnestus",
				life: 3000
			});
			failedAny = true;
		} else {
			catData.value = catEditRes.data;
		}

		// can be undefined, foster home could be selected as none -> nothing updated
		if ( fosterHomeEditRes ) {
			if ( !fosterHomeEditRes.data ) {
				toast.add({
					severity: "error",
					summary: "Hoiukodu uuendamine ebaonnestus",
					life: 3000
				});
				failedAny = true;
			} else {
				// update foster home fields in options
				const fosterHomeUpdatedIdx = catManagementFieldOptions.value.foster_homes.findIndex( fh => fh.id === fosterHomeEditRes.data.id );

				if ( fosterHomeUpdatedIdx === -1 ) {
					console.error( "failed to update foster home options" )
				} else {
					catManagementFieldOptions.value.foster_homes[ fosterHomeUpdatedIdx ] = fosterHomeEditRes.data;
				}
			}
		}

		return !failedAny;
	},
	notes: async ( ) => {
		if ( !catData.value ) {
			toast.add({
				severity: "warn",
				summary: "Kassi pole.",
				life: 3000
			});
			return false;
		}

		const res = await api.updateCatCatsCatIdPatch({
			body: {
				payload: JSON.stringify({
					notes: catNotes.value
				} as CatUpdate )
			},
			path: {
				cat_id: catData.value.id
			}
		});

		if ( !res.data ) {
			toast.add({
				severity: "error",
				summary: "Kassi uuendamine ebaonnestus",
				life: 3000
			});

			return false;
		}

		catData.value = res.data;

		return true;
	}
}

const submitEdit = async ( what: EditableFields ) => {
	if ( editing.value[ what ] === EditingStatus.EDITING ) {
		if ( !saveField[ what ] ) console.warn( `no save callback function for "${ what }" exists, can't save."` );
		else {
			editing.value[ what ] = EditingStatus.SUBMITTING;
			const res = await saveField[ what ]();

			if ( !res ) console.error( `save callback for "${ what }" failed` );
		}

		editing.value[ what ] = EditingStatus.IDLE;
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
			} );
			return;
		}

		catData.value = res.data;

		syncCatStatusToCatData( res.data );
		syncMainEditFieldsToCatData( res.data );
		syncCatManagementFieldsToCatData( res.data );
		syncCatNotesFieldsToCatData( res.data );
	} )
}

watch(
	() => router.currentRoute.value.params.id,
	( newId ) => fetchCatInfo( newId )
);

watch(
	( ) => catProfilePicture.value,
	async ( newPfp ) => {
		if ( !newPfp ) return;

		if ( editing.value.pfp === EditingStatus.IDLE ) {
			editing.value.pfp = EditingStatus.EDITING;
			await submitEdit( "pfp" );
		}
	}
);

watch(
	( ) => catPfpImgRef.value,
	async ( ) => {
		await updateCatProfileImage( );
	}
)

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