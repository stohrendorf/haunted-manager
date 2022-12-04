<script lang="ts">
import { ITag } from "@/components/ApiService";
import BsTooltip from "@/components/bootstrap/BsTooltip";
import { PropType, defineComponent } from "vue";

export default defineComponent({
  directives: {
    BsTooltip,
  },
  props: {
    tags: {
      type: Array as PropType<ITag[]>,
      required: true,
    },
  },
});
</script>

<template>
  <div>
    <span
      v-for="tag in tags"
      :key="tag.name"
      v-bs-tooltip
      :title="tag.description"
      class="badge bg-secondary me-1"
    >
      {{ tag.name }}
    </span>
  </div>
</template>

<style scoped></style>
