<script lang="ts">
import { Options, Vue } from "vue-class-component";

@Options({})
export default class BsDropdownNavItem extends Vue {}
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
    <div class="dropdown-menu dropdown-menu-end">
      <slot />
    </div>
  </li>
</template>

<style scoped>
.dropdown-menu {
  width: 300px;
}
</style>
