<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    modelValue: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: true,
    },
    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },
    required: {
      type: Boolean,
      required: false,
      default: false,
    },
    placeholder: {
      type: String,
      required: false,
      default: "",
    },
    type: {
      type: String,
      required: false,
      default: "text",
    },
  },
});
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
