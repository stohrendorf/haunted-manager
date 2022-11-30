<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    percent: {
      type: Number,
      required: true,
    },
  },
});
</script>

<template>
  <div
    class="progress-bar"
    role="progressbar"
    :style="'width: ' + percent + '%'"
  >
    <slot />
  </div>
</template>

<style scoped></style>
