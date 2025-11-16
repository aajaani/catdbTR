<script setup lang="ts">
const model = defineModel< File | null >({
	required: true
});
</script>

<template>
	<button
		class="relative"
	>
		Lae pilt ules
		<input
			type="file"
			class="absolute inset-0 opacity-0 cursor-pointer"
			accept="image/*"
			@change="ev => {
				const tgt = ev.target as HTMLInputElement;

				if ( !tgt || !tgt.files || tgt.files?.length === 0 ) return;

				model = tgt.files[ 0 ] || null;
			}"
		>
	</button>
</template>

<style scoped lang="css">

</style>