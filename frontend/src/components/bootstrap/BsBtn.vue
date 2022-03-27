<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { Prop } from "vue-property-decorator";
import { Variant } from "./BsTypes";

@Options({})
export default class BsBtn extends Vue {
  @Prop({ required: true })
  public variant!: Variant;

  @Prop({ required: false, default: false, type: Boolean })
  public disabled: boolean = undefined!;

  @Prop({ required: false, default: false, type: Boolean })
  public small: boolean = undefined!;
}
</script>

<template>
  <button
    :class="[
      'btn',
      'btn-' + variant,
      disabled ? 'disabled' : '',
      small ? 'btn-sm' : '',
    ]"
    type="button"
    :disabled="disabled"
  >
    <slot />
  </button>
</template>

<style scoped></style>
