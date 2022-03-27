<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { Prop } from "vue-property-decorator";
import { Variant } from "./BsTypes";

@Options({})
export default class BsAlert extends Vue {
  @Prop({ required: true }) public variant!: Variant;
}
</script>

<template>
  <div :class="['alert', 'alert-' + variant]" role="alert">
    <slot />
  </div>
</template>

<style scoped></style>
