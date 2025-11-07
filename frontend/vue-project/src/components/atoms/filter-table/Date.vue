<template>
  <span
    v-if="!isEditing"
    @click.alt="isEditing = true"
  >
    {{  props.date ?? "-"  }}
  </span>

  <div
   v-else
   class="flex gap-1"
  >
    <input
        type="date"
        class="input outline-none max-w-32"
        v-model="editedValue"
    />
    <Button
      class="accept"
      @click="( ) => {
        if ( props.onEditAccept && editedValue )
          props.onEditAccept( editedValue );

        isEditing = false;
      }"
    >
      <FiCheck size="20" />
    </Button>

    <Button
      class="destructive"
      @click="( ) => {
        if ( props.onEditCancel )
          props.onEditCancel( );

        isEditing = false;
      }"
    >
      <FiX size="20" />
    </Button>
  </div>

</template>

<script setup lang="ts">
import { FiCheck, FiX } from "vue-icons-plus/fi";
import Button from "@/components/atoms/Button.vue"
import { ref, watch } from "vue";

const props = defineProps<{
  date: string | null,
  isEditing?: boolean,
  onEditAccept?: ( newDate: string ) => void,
  onEditCancel?: ( ) => void,
}>( );

// todo: check filter-table/Text.vue
const isEditing = ref< boolean >( props.isEditing ?? false );
const editedValue = ref< string | null >( props.date );

// whenever props change, reflect isEditing
watch(
    ( ) => props.isEditing,
    ( newVal ) => {
      isEditing.value = newVal;

      if ( newVal ) {
        editedValue.value = props.date;
      }
    }
)
</script>

<style lang="css" scoped>

</style>