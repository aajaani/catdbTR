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
		class="pl-2"
	>{{ props.text }}</p>

	<textarea
		v-else
		v-model="model"
		class="w-full px-2 py-1 pt-[1px] bg-transparent outline-none border-table-border border-[1px] border-solid rounded-md"
		spellcheck="false"
	></textarea>
</template>

<style scoped lang="css">
textarea:disabled {
	color: #888;
	opacity: 0.4;
}
</style>