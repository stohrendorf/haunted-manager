<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  props: {
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
    label: {
      type: String,
      required: true,
    },
    modelValue: {
      type: String,
      required: true,
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
    <span class="input-group-text">{{ label }}</span>
    <input
      :value="modelValue"
      :type="type"
      class="form-control"
      :placeholder="label"
      :aria-label="label"
      :disabled="disabled"
      :required="required"
      @input="$emit('update:modelValue', $event.target.value)"
    />
    <slot />
  </div>
</template>

<style scoped></style>
