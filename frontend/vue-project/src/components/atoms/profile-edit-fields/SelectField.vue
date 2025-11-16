<script setup lang="ts">
type SelectFieldProps = {
	defaultSelected: number,
	options: { [ key: number ]: string },
	isEditing?: boolean,
}

const props = defineProps<SelectFieldProps>();

const model = defineModel<number>( {
	required: true,
	default( props: SelectFieldProps ) {
		return props.defaultSelected
	}
} );
</script>

<template>
	<p
		v-if="!props.isEditing"
	>{{ props.options[ props.defaultSelected ] }}</p>

	<select
		v-else
		@change="( event: Event ) => {
			try {
				model = parseInt( ( event.target as HTMLSelectElement ).value );
			} catch ( _ ) {
				console.error( 'SelectField.vue - failed to parse selected field value' );
			}
		}"
		class="text-right w-fit underline pr-2 bg-transparent outline-none border-table-border border-[1px] border-solid rounded-md pt-[3px] pb-[2px]"
	>
		<option
			v-for="( option, key ) in options"
			:key="`${ key }-${ option }`"
			:value="key"
			:selected="parseInt( key ) === model"
		>{{ option }}
		</option>
	</select>
</template>

<style scoped lang="css">
select:disabled {
	color: #888;
	opacity: 0.4;
}
</style>