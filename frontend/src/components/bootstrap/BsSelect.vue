<script lang="ts">
import { ISelectEntry } from "@/components/bootstrap/ISelectEntry";
import { defineComponent, PropType } from "vue";

export default defineComponent({
  props: {
    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },
    label: {
      type: String,
      required: true,
    },
    modelValue: {
      type: [String, Number, Boolean],
      required: true,
    },
    items: {
      type: Object as PropType<ISelectEntry[]>,
      required: true,
    },
  },
  data() {
    return {
      selectedValue: null as any | null,
    };
  },
  created() {
    this.selectedValue = this.modelValue;
  },
  methods: {
    updatedSelection() {
      this.$emit("update:modelValue", this.selectedValue);
    },
  },
});
</script>

<template>
  <select
    v-model="selectedValue"
    class="form-select"
    :aria-label="label"
    :disabled="disabled"
    @change="updatedSelection()"
  >
    <option v-for="item in items" :key="item" :value="item.value">
      {{ item.title }}
    </option>
  </select>
</template>

<style scoped></style>
