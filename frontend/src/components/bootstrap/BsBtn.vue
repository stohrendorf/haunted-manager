<script lang="ts">
import { Variant } from "./BsTypes";
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    variant: {
      type: Variant,
      required: true,
    },
    disabled: {
      type: Boolean,
      default: false,
      required: false,
    },
    small: {
      type: Boolean,
      default: false,
      required: false,
    },
    outline: {
      type: Boolean,
      default: false,
      required: false,
    },
  },
});
</script>

<template>
  <button
    :class="[
      'btn',
      'btn-' + (outline ? 'outline-' : '') + variant,
      disabled ? 'disabled' : '',
      small ? 'btn-sm' : '',
    ]"
    type="button"
    :disabled="disabled"
  >
    <slot />
  </button>
</template>

<style scoped></style>
