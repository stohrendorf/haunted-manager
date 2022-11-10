<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { Prop } from "vue-property-decorator";

@Options({})
export default class BsDropdownNavItem extends Vue {
  @Prop({ required: false, default: null })
  public minWidth!: string | null;

  @Prop({ required: false, default: false })
  public end!: boolean;
}
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
      :class="['dropdown-menu', end ? 'dropdown-menu-end' : '']"
      :style="minWidth !== null ? 'min-width:' + minWidth : ''"
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
