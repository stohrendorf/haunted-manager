<script lang="ts">
import { ITag, getTags } from "@/components/ApiService";
import BsCheckboxMultiple from "@/components/bootstrap/BsCheckboxMultiple.vue";
import { PropType, defineComponent } from "vue";

export default defineComponent({
  components: {
    BsCheckboxMultiple,
  },
  props: {
    modelValue: {
      type: Array as PropType<ITag[]>,
      required: true,
    },
  },
  emits: ["saved", "update:modelValue"],
  data() {
    return {
      tags: null as ITag[] | null,
      selectedTags: [] as ITag[],
    };
  },
  async created(): Promise<void> {
    this.tags = (await getTags()).tags;
    this.selectedTags = [...this.modelValue];
    this.$watch(
      () => this.modelValue,
      () => {
        this.selectedTags = [...this.modelValue];
      }
    );
  },
});
</script>

<template>
  <ul class="list-unstyled">
    <li v-for="tag in tags" :key="tag.id">
      <bs-checkbox-multiple
        v-model="selectedTags"
        :value="tag"
        @change="$emit('update:modelValue', selectedTags)"
      >
        <span class="badge bg-secondary">{{ tag.name }}</span>
        {{ tag.description }}
      </bs-checkbox-multiple>
    </li>
  </ul>
</template>

<style scoped></style>
