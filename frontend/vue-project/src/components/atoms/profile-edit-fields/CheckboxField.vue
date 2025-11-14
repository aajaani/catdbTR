<script setup lang="ts">
const props = defineProps<{
	defaultChecked: boolean,
	isEditing?: boolean
}>();

const model = defineModel<boolean>( {
	required: true
} );
</script>

<template>
	<input
		v-if="!props.isEditing"
		type="checkbox"
		:checked="props.defaultChecked"
		disabled
	>

	<div
		v-else
		class="pr-2 pt-[1px] pb-[3px]"
	>
		<input
			type="checkbox"
			v-model="model"
		>
	</div>

</template>

<style scoped lang="css">
input:invalid {
	@apply border-red-600;
}
</style>