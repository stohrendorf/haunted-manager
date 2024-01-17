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
      small ? 'smaller-button' : '',
    ]"
    type="button"
    :disabled="disabled"
  >
    <slot />
  </button>
</template>

<style scoped>
.smaller-button {
  --bs-btn-padding-y: 0.25rem;
  --bs-btn-padding-x: 0.5rem;
  --bs-btn-font-size: 0.75rem;
}
</style>
