<template>
  <button
    class="px-2.5 py-auto border-neutral-400 border-[1px] rounded-[8px] flex gap-2 justify-center items-center uppercase text-[14px]"
  >
    <slot name="icon"></slot>
    <slot></slot>
  </button>
</template>

<style scoped>
button {
  min-height: 40px;

  &.small {
    @apply rounded-full bg-border-group capitalize py-0 leading-[18px];
    min-height: fit-content;
  }
}

button.primary {
  @apply border-primary-normal bg-primary-normal text-text-button;
}

button.secondary {
  @apply border-[color-mix(in_srgb,theme(colors.primary.normal)_50%,white)] bg-[color-mix(in_srgb,theme(colors.primary.normal)_50%,white)] text-black;
}
</style>