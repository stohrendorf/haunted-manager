<script lang="ts">
import { DateTime, TempusDominus } from "@eonasdan/tempus-dominus";
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    modelValue: {
      type: String,
      required: true,
    },
  },
  emits: ["update:modelValue"],
  mounted(): void {
    const picker = new TempusDominus(this.$refs.picker as HTMLDivElement, {
      viewDate: new DateTime(this.modelValue),
      defaultDate: new DateTime(this.modelValue),
      display: {
        theme: "light",
        sideBySide: true,
        components: {
          hours: true,
          minutes: true,
        },
      },
    });
    picker.subscribe("change.td", (x) => {
      this.$emit("update:modelValue", (x.date as Date).toISOString());
    });
  },
});
</script>

<template>
  <div :id="'htmlTarget' + $.uid">
    <span ref="picker" style="display: inline-block">
      <span class="btn btn-outline-primary">
        <span class="bi bi-calendar3" aria-hidden="true"></span>
        <slot />
      </span>
    </span>
  </div>
</template>

<style scoped>
@import "@eonasdan/tempus-dominus/dist/css/tempus-dominus.css";
@import "@fortawesome/fontawesome-free/css/all.css";
</style>
