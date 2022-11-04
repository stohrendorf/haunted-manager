<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { Prop } from "vue-property-decorator";
import { Variant } from "./BsTypes";

@Options({})
export default class BsNavbar extends Vue {
  @Prop({ required: true, default: "dark" })
  public variant!: Variant;
}
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
