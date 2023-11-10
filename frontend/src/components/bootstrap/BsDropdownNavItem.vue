<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    minWidth: {
      type: String,
      required: false,
      default: null,
    },
    end: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
});
</script>

<template>
  <li class="nav-item dropdown">
    <a
      data-bs-toggle="dropdown"
      class="nav-link dropdown-toggle"
      role="button"
      aria-expanded="false"
    >
      <slot name="toggle" />
    </a>
    <div
      :class="['dropdown-menu', { 'dropdown-menu-end': end }]"
      :style="minWidth ? `min-width: ${minWidth}` : ''"
    >
      <slot />
    </div>
  </li>
</template>

<style scoped>
.dropdown-menu {
  width: 300px;
}
</style>
