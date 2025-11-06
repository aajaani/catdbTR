<template>
  <span
    v-if="!isEditing"
  >
    {{  props.text  }}
  </span>

  <div
   v-else
   class="flex gap-1"
  >
    <input
        type="text"
        class="input outline-none max-w-32"
        v-model="editedValue"
    />
    <Button
      class="accept"
      @click="( ) => {
        if ( props.onEditAccept )
          props.onEditAccept( editedValue );
      }"
    >
      <FiCheck size="20" />
    </Button>

    <Button
      class="destructive"
      @click="( ) => {
        if ( props.onEditCancel )
          props.onEditCancel( );
      }"
    >
      <FiX size="20" />
    </Button>
  </div>

</template>

<script setup lang="ts">
import { FiCheck, FiX } from "vue-icons-plus/fi";
import Button from "@/components/atoms/Button.vue"
import { ref } from "vue";

const props = defineProps<{
  text: string,
  isEditing?: boolean,
  onEditAccept?: ( newText: string ) => void,
  onEditCancel?: ( ) => void,
}>( );

const editedValue = ref<string>( props.text );
</script>

<style lang="css" scoped>

</style>