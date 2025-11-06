<template>
  <span class="flex flex-row items-center gap-2">
    <span class="w-3 h-3 min-h-3 min-w-3 rounded-full status-circle" :data-color="props.color">

    </span>
    <span
      v-if="props.label && !props.isEditing"
      class="text-table-normal"
    >{{ props.label }}</span>

    <select
      v-else-if="props.label && props.isEditing"
      class="text-table-normal border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-gray-400"
      @change="( event ) => {
        const tgt = event.target as HTMLSelectElement;
        const newCodeName = tgt.value as string;
        const newPrettyName = props.options && props.options[ newCodeName ]
                                ? props.options[ newCodeName ]
                                : newCodeName;
        if ( props.onChange )
          props.onChange( newCodeName, newPrettyName );
      }"
    >
      <option
        v-for="( optLabel, codeName ) in props.options"
        :key="codeName"
        :value="codeName"
        :selected="label === optLabel"
      >{{ optLabel }}</option>
    </select>
  </span>
</template>

<script setup lang="ts">
type ColorOption = "green" | "yellow" | "red" | "black" | "gray";

// inner name to readable name mapping
type OptionsType = { [ underlyingName: string ]: string };

const props = defineProps<{
  color: ColorOption,
  label?: string
  isEditing?: boolean,
  options?: OptionsType,
  onChange?: ( codeName: string, prettyName: string ) => void,
}>( )
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