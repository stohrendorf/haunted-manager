<script lang="ts">
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import { defineComponent } from "vue";

export default defineComponent({
  components: { BsBtn },
  props: {
    value: {
      type: String,
      required: true,
    },
  },
  methods: {
    async copyToClipboard(): Promise<void> {
      await navigator.clipboard.writeText(this.value);
    },
  },
});
</script>

<template>
  <div style="display: inline-block; white-space: nowrap">
    <slot />&hairsp;<bs-btn variant="primary" small @click="copyToClipboard()">
      <span class="bi bi-clipboard" />
    </bs-btn>
  </div>
</template>

<style scoped></style>
