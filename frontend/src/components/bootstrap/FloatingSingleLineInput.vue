<script lang="ts">
import { Vue } from "vue-class-component";
import { Prop } from "vue-property-decorator";

export default class FloatingSingleLineInput extends Vue {
  @Prop({ default: () => "", required: true, type: String })
  public modelValue!: string;
  @Prop({ default: false })
  public disabled!: boolean;
  @Prop({ default: false })
  public required!: boolean;
  @Prop({ required: true })
  public label!: string;
  @Prop({ required: false, default: "" })
  public placeholder!: string;
  @Prop({ required: false, default: "text" })
  public type!: string;
}
</script>

<template>
  <div :class="{ 'input-group': true, disabled: disabled }">
    <div class="form-floating">
      <input
        :id="'input--' + $.uid"
        :value="modelValue"
        :type="type"
        class="form-control"
        :placeholder="placeholder"
        :aria-label="label"
        :disabled="disabled"
        :aria-disabled="disabled"
        :required="required"
        :aria-required="required"
        @input="$emit('update:modelValue', $event.target.value)"
      />
      <label :for="'input--' + $.uid">{{ label }}</label>
    </div>
    <slot />
  </div>
</template>

<style scoped></style>
