<script lang="ts">
import { Variant } from "./BsTypes";
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    variant: {
      type: Variant,
      required: false,
      default: "dark",
    },
  },
});
</script>

<template>
  <nav
    :class="['navbar', 'navbar-expand', 'navbar-' + variant, 'bg-' + variant]"
  >
    <div class="container-fluid">
      <a
        class="navbar-brand"
        style="cursor: pointer"
        @click="$router.push('/')"
      >
        <slot name="brand" />
      </a>

      <div class="navbar-collapse collapse">
        <slot />
      </div>
    </div>
  </nav>
</template>

<style scoped></style>
