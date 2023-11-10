<script lang="ts">
import { defineComponent } from "vue";
import * as _ from "lodash";

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
  data() {
    return {
      localModelValue: [] as any[],
    };
  },
  computed: {
    checked: {
      get(): boolean {
        return this.localModelValue.some((x) => _.isEqual(x, this.value));
      },
      set(value: boolean) {
        if (
          value &&
          !this.localModelValue.some((x) => _.isEqual(x, this.value))
        ) {
          this.localModelValue.push(this.value);
        } else if (
          !value &&
          this.localModelValue.some((x) => _.isEqual(x, this.value))
        ) {
          this.localModelValue.splice(
            this.localModelValue.findIndex((x) => _.isEqual(x, this.value)),
            1,
          );
        } else {
          return;
        }
        this.$emit("update:modelValue", this.localModelValue);
      },
    },
  },
  created: function (): void {
    this.localModelValue = [...this.modelValue];
    this.$watch(
      () => this.modelValue,
      () => {
        this.localModelValue = [...this.modelValue];
      },
    );
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
