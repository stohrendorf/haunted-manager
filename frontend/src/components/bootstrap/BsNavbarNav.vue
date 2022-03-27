<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { Prop } from "vue-property-decorator";

@Options({})
export default class BsNavbarNav extends Vue {
  @Prop({ required: false, default: "" })
  public ms!: "auto" | "5" | "4" | "3" | "2" | "1";
}
</script>

<template>
  <ul :class="['navbar-nav', 'nav-pills', ms ? 'ms-' + ms : '']">
    <slot />
  </ul>
</template>

<style scoped></style>
