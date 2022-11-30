<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    value: {
      type: [Object, Boolean, String, Number, Date, Array],
      required: false,
      default: true,
    },
    modelValue: {
      type: Array,
      required: false,
      default() {
        return [];
      },
    },
  },
  emits: ["onChecked", "update:modelValue"],
  data() {
    return {
      checked: false,
    };
  },
  created(): void {
    const updateChecked = () => {
      const value = JSON.stringify(this.value);
      this.checked = this.modelValue.some((x) => JSON.stringify(x) == value);
      this.$emit("onChecked", this.checked);
    };

    this.$watch(() => this.modelValue, updateChecked);
    this.$watch(() => this.value, updateChecked);
    updateChecked();
  },
  methods: {
    changed(): void {
      const checked = (
        document.getElementById(String(this.$.uid)) as HTMLInputElement
      ).checked;
      const value = JSON.stringify(this.value);
      if (checked && !this.modelValue.some((x) => JSON.stringify(x) == value))
        this.$emit("update:modelValue", this.modelValue?.concat(this.value));
      else if (
        !checked &&
        this.modelValue.some((x) => JSON.stringify(x) == value)
      ) {
        this.$emit(
          "update:modelValue",
          this.modelValue?.filter((x) => JSON.stringify(x) !== value)
        );
      } else return;
      this.$emit("update:modelValue", this.modelValue);
      this.checked = checked;
      this.$emit("onChecked", this.checked);
    },
  },
  emit: ["onChecked"],
});
</script>

<template>
  <div class="form-check form-check-inline">
    <input
      :id="$.uid"
      v-model="checked"
      class="form-check-input"
      type="checkbox"
      :value="value"
      @input="changed"
    />
    <label :for="$.uid"><slot /></label>
  </div>
</template>

<style scoped></style>
