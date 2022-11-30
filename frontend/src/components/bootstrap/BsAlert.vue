<script lang="ts">
import { Variant } from "./BsTypes";
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    variant: {
      type: Variant,
      required: true,
    },
  },
});
</script>

<template>
  <div :class="['alert', 'alert-' + variant]" role="alert">
    <slot />
  </div>
</template>

<style scoped></style>
