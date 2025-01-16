<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    modelValue: {
      type: Boolean,
      required: true,
    },
  },
  emits: ["update:modelValue"],
  data() {
    return {
      checked: false,
    };
  },
  created() {
    this.checked = this.modelValue;
    this.$watch("modelValue", () => (this.checked = this.modelValue));
    this.$watch("checked", () => this.$emit("update:modelValue", this.checked));
  },
});
</script>

<template>
  <div class="form-check form-check-inline">
    <input
      :id="$.uid + ''"
      v-model="checked"
      class="form-check-input"
      type="checkbox"
    />
    <label :for="$.uid + ''">
      <slot />
    </label>
  </div>
</template>

<style scoped></style>
