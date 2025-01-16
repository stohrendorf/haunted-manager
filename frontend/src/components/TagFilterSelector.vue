<script lang="ts">
import { ITag } from "@/components/ApiService";
import TagsSelector from "@/components/TagsSelector.vue";
import BsTooltip from "@/components/bootstrap/BsTooltip";
import { PropType, defineComponent } from "vue";

export default defineComponent({
  directives: {
    BsTooltip,
  },
  components: {
    TagsSelector,
  },
  props: {
    modelValue: {
      type: Array as PropType<ITag[]>,
      required: true,
    },
    availableTags: {
      type: Array as PropType<ITag[]>,
      required: true,
    },
  },
  emits: ["update:modelValue"],
  data() {
    return {
      filterTags: [] as ITag[],
    };
  },
  async created() {
    this.filterTags = [...this.modelValue];
    this.$watch(
      () => this.modelValue,
      () => {
        this.filterTags = [...this.modelValue];
      },
    );
  },
});
</script>

<template>
  <div class="dropdown">
    <button
      type="button"
      data-bs-toggle="dropdown"
      aria-expanded="false"
      class="btn btn-primary dropdown-toggle"
    >
      <span v-show="filterTags.length === 0">
        <span class="bi bi-funnel" />
        <span> No Tag Filter </span>
      </span>

      <span v-show="filterTags.length !== 0">
        <span class="bi bi-funnel-fill" />
        <span>
          All of
          <span
            v-for="tag in filterTags"
            :key="tag.name"
            v-bs-tooltip
            :title="tag.description"
            class="badge bg-secondary ms-1"
          >
            {{ tag.name }}
          </span>
        </span>
      </span>
    </button>
    <div class="dropdown-menu">
      <tags-selector
        v-model="filterTags"
        class="ms-2"
        :available-tags="availableTags"
        @update:model-value="$emit('update:modelValue', filterTags)"
      />
    </div>
  </div>
</template>

<style scoped></style>
