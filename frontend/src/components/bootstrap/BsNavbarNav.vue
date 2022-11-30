<script lang="ts">
import { defineComponent } from "vue";
import { Ms } from "@/components/bootstrap/BsTypes";

export default defineComponent({
  props: {
    ms: {
      type: Ms,
      required: false,
      default: null,
    },
  },
});
</script>

<template>
  <ul :class="['navbar-nav', 'nav-pills', ms ? 'ms-' + ms : '']">
    <slot />
  </ul>
</template>

<style scoped></style>
