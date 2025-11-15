<script setup lang="ts">
const props = defineProps<{
	text: string,
	isEditing?: boolean
}>();

const model = defineModel<string>( {
	required: true
} );
</script>

<template>
	<p
		v-if="!props.isEditing"
	>{{ props.text }}</p>

	<input
		v-else
		v-model="model"
		class="text-right w-fit underline pr-2 bg-transparent outline-none border-table-border border-[1px] border-solid rounded-md p-[1px]"
	>
</template>

<style scoped lang="css">
input:invalid {
	@apply border-red-600;
}

input[type=date] {
	@apply pl-2;
}


input:disabled {
	color: #888;
	opacity: 0.4;
}
</style>