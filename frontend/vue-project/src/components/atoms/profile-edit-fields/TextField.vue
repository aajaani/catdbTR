<script setup lang="ts">
import { nextTick, ref, watch } from "vue";

const props = defineProps<{
	text: string,
	isEditing?: boolean
}>();

const model = defineModel<string>( {
	required: true
} );

const previewRef = ref< HTMLElement | null>( null );
const textAreaRef = ref< HTMLTextAreaElement | null >( null );

watch(
	( ) => props.isEditing,
	async ( newIsEditing ) => {
		if ( !newIsEditing ) return;
		await nextTick( );

		if ( textAreaRef.value ) {
			autoResize( textAreaRef.value );

			textAreaRef.value.focus( );
			textAreaRef.value.setSelectionRange( textAreaRef.value.value.length, textAreaRef.value.value.length );
		}
	}
);

const autoResize = ( el: HTMLTextAreaElement ) => {
	el.style.height = "auto";

	// gahahahahah
	// I love js
	// getComputedStyle causes it to update layout
	// if we don't access cs.height, cs is omitted and
	// layout update is never performed
	const cs = getComputedStyle(el);
	cs.height;

	const target = Math.max( el.scrollHeight + parseFloat( cs.paddingTop ) + parseFloat( cs.paddingBottom ), 0 );

	// set in a reqanimframe
	// without this wouldn't work, either race or layout trash
	requestAnimationFrame( ( ) => {
		el.style.height = `${target}px`;
	} );
}
</script>

<template>
	<div
		v-if="!props.isEditing"
		ref="previewRef"
	>
		<p
			v-for="text of props.text.split( '\n' )"
			v-if="!props.isEditing"
			class="pl-2"
		>
			<br v-if="text.length === 0" />
			<span v-else>{{ text }}</span>
		</p>
	</div>


	<textarea
		v-else
		ref="textAreaRef"
		v-model="model"
		class="w-full px-[7px] py-[1px] bg-transparent outline-none border-table-border border-[1px] border-solid rounded-md"
		spellcheck="false"
		@input="ev => autoResize( ev.target as HTMLTextAreaElement )"
	></textarea>
</template>

<style scoped lang="css">
textarea {
	overflow: hidden;
	resize: none;
}

textarea:disabled {
	color: #888;
	opacity: 0.4;
}
</style>