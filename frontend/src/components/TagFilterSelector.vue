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
      }
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
      <span class="bi bi-filter" />
      <span v-show="filterTags.length === 0"> No Filter </span>
      <span v-show="filterTags.length !== 0">
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
    </button>
    <div class="dropdown-menu">
      <tags-selector
        v-model="filterTags"
        class="ms-2"
        :available-tags="availableTags"
        @change="$emit('update:modelValue', filterTags)"
      />
    </div>
  </div>
</template>

<style scoped></style>
