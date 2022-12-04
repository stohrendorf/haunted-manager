<script lang="ts">
import {
  IGhostFileResponseEntry,
  ITag,
  getAlternativeLevels,
  getTags,
  updateGhost,
} from "@/components/ApiService";
import TagsSelector from "@/components/TagsSelector.vue";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import BsCheckboxSingle from "@/components/bootstrap/BsCheckboxSingle.vue";
import BsSelect from "@/components/bootstrap/BsSelect.vue";
import FloatingSingleLineInput from "@/components/bootstrap/FloatingSingleLineInput.vue";
import { ISelectEntry } from "@/components/bootstrap/ISelectEntry";
import { PropType, defineComponent } from "vue";

export default defineComponent({
  components: {
    TagsSelector,
    BsSelect,
    BsBtn,
    FloatingSingleLineInput,
    BsCheckboxSingle,
  },
  props: {
    modelValue: {
      type: Object as PropType<IGhostFileResponseEntry>,
      required: true,
    },
  },
  emits: ["saved", "update:modelValue"],
  data() {
    return {
      tags: null as ITag[] | null,
      alternativeLevels: null as ISelectEntry[] | null,
      localGhost: null as IGhostFileResponseEntry | null,
    };
  },
  async created(): Promise<void> {
    this.localGhost = JSON.parse(JSON.stringify(this.modelValue));
    this.$watch(
      () => this.modelValue,
      () => {
        this.localGhost = JSON.parse(JSON.stringify(this.modelValue));
      }
    );

    this.tags = (await getTags()).tags;
    this.alternativeLevels = (
      await getAlternativeLevels(this.modelValue.level_identifier)
    ).levels.map((x) => ({ value: x.id, title: x.title }));
  },
  methods: {
    async saveGhost(): Promise<void> {
      await updateGhost(this.localGhost!.id, {
        published: this.localGhost!.published,
        tags: this.localGhost!.tags.map((tag) => tag.id),
        description: this.localGhost!.description,
        level_id: this.localGhost!.level_id,
      });
      this.updated();
      this.$emit("saved");
    },

    updated() {
      this.$emit("update:modelValue", this.localGhost);
    },
  },
});
</script>

<template>
  <div>
    <div class="row">
      <div class="col">
        <bs-select
          v-model="localGhost.level_id"
          :items="alternativeLevels"
          label="Level"
          @change="updated()"
        />
        <span class="bi bi-stopwatch"></span>
        {{ $filters.seconds(localGhost.duration) }}
        &bull;
        <bs-checkbox-single v-model="localGhost.published" @change="updated()">
          <span class="bi bi-cloud" /> Published
        </bs-checkbox-single>
      </div>
    </div>
    <floating-single-line-input
      v-model="localGhost.description"
      class="row"
      label="Description"
      @change="updated()"
    />
    <tags-selector v-model="localGhost.tags" class="row" />
    <div class="row row-cols-auto">
      <bs-btn variant="success" small @click="saveGhost()">
        <span class="bi bi-save"></span> Save
      </bs-btn>
      <slot />
    </div>
  </div>
</template>

<style scoped></style>
