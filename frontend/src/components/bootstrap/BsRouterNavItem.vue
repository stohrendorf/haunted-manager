<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    to: {
      type: String,
      required: true,
    },
    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
});
</script>

<template>
  <li class="nav-item">
    <router-link :to="to" class="nav-link" :class="{ disabled: disabled }">
      <slot />
    </router-link>
  </li>
</template>

<style scoped></style>
