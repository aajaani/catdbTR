<template>
  <span class="flex flex-row items-center gap-2">
    <span
		v-if="props.color"
		class="w-3 h-3 min-h-3 min-w-3 rounded-full status-circle"
		:data-color="props.color"
		@click.alt="isEditing = !props.disableEditWithAlt"
	/>

    <span
		v-if="props.label && !isEditing"
		class="text-table-normal"
		@click.alt="isEditing = !props.disableEditWithAlt"
	>{{ props.label }}</span>

    <select
		v-else-if="props.label && isEditing"
		class="text-table-normal border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-gray-400"
		@change="( event ) => {
        const tgt = event.target as HTMLSelectElement;
        const selectedOption = Object.entries( options ).find( ( ([ key, _ ]) => key === tgt.value ) );

        if ( !selectedOption ) {
          console.error( `[Selection.vue] failed to parse selected option value: ${ tgt.value }` );
          return;
        }

        props.onChange?.( selectedOption[ 1 ], selectedOption[ 0 ] );
        isEditing = false;
      }"
	>
      <option
		  v-for="( codeName, optLabel ) in options"
		  :key="`${ codeName }-option`"
		  :value="optLabel"
		  :selected="label === optLabel"
	  >{{ optLabel }}</option>
    </select>
  </span>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";

type ColorOption = "green" | "yellow" | "red" | "black" | "gray";

type Options = Record<string, string | number | boolean>;
type OptionsAsync = () => Promise<Options>;

const props = defineProps<{
	color?: ColorOption;
	label?: string;
	isEditing?: boolean;
	options?: Options | OptionsAsync;
	onChange?: ( key: Options[ string ], prettyName: string ) => void;
	disableEditWithAlt?: boolean
}>();

// todo: check filter-table/Text.vue
const isEditing = ref<boolean>( props.isEditing ?? false );
const options = ref<Options>( {} as Options );

watch(
	() => isEditing.value,
	async ( newVal ) => {
		// only fetch options when entering editing mode
		if ( newVal ) {
			// options is fetched async
			if ( typeof props.options === "function" ) {
				options.value = await props.options();
			} else
				options.value = props.options || {};
		}
	},
	{ immediate: true }
)

// whenever props change, reflect isEditing
watch(
	() => props.isEditing,
	( newVal ) => {
		isEditing.value = newVal;
	}
)
</script>

<style lang="css" scoped>
.status-circle[data-color="green"] {
	background-color: #56BA28;
}

.status-circle[data-color="yellow"] {
	background-color: #FEBC2F;
}

.status-circle[data-color="red"] {
	background-color: #FF5F57;
}

.status-circle[data-color="black"] {
	background-color: #404040;
}

.status-circle[data-color="gray"] {
	background-color: #8C8C8C;
}
</style>