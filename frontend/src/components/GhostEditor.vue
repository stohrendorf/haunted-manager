<script lang="ts">
import { Options, Vue } from "vue-class-component";
import {
  getTags,
  IGhostFileResponseEntry,
  ITag,
  updateGhost,
  getAlternativeLevels,
} from "@/components/ApiService";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import FloatingSingleLineInput from "@/components/bootstrap/FloatingSingleLineInput.vue";
import BsCheckboxMultiple from "@/components/bootstrap/BsCheckboxMultiple.vue";
import { Emit, Prop } from "vue-property-decorator";
import DateTimePicker from "@/components/utilities/DateTimePicker.vue";
import BsCheckboxSingle from "@/components/bootstrap/BsCheckboxSingle.vue";
import BsSelect from "@/components/bootstrap/BsSelect.vue";
import { ISelectEntry } from "@/components/bootstrap/ISelectEntry";

@Options({
  components: {
    BsSelect,
    BsCheckboxMultiple,
    BsBtn,
    FloatingSingleLineInput,
    DateTimePicker,
    BsCheckboxSingle,
  },
})
export default class GhostEditor extends Vue {
  private tags: ITag[] | null = null;
  private alternativeLevels: ISelectEntry[] = [];

  @Prop({ required: true, default: () => ({ tags: [] }) })
  public ghost!: IGhostFileResponseEntry;

  async created(): Promise<void> {
    this.tags = (await getTags()).tags;
    this.alternativeLevels = (
      await getAlternativeLevels(this.ghost.level_identifier)
    ).levels.map((x) => ({ value: x.id, title: x.title }));
  }

  async saveGhost(): Promise<void> {
    await updateGhost(this.ghost.id, {
      published: this.ghost.published,
      tags: this.ghost.tags.map((tag) => tag.id),
      description: this.ghost.description,
      level_id: this.ghost.level_id,
    });
    this.saved();
  }

  onPublishedChecked(value: boolean): void {
    this.ghost.published = value;
  }

  @Emit()
  saved(): void {}
}
</script>

<template>
  <div>
    <div class="row">
      <div class="col">
        <bs-select
          v-model="ghost.level_id"
          :items="alternativeLevels"
          label="Level"
        />
        <span class="bi bi-stopwatch"></span>
        {{ $filters.seconds(ghost.duration) }}
        &bull;
        <bs-checkbox-single v-model="ghost.published">
          <span class="bi bi-cloud" /> Published
        </bs-checkbox-single>
      </div>
    </div>
    <div class="row">
      <floating-single-line-input
        v-model="ghost.description"
        label="Description"
      ></floating-single-line-input>
    </div>
    <div class="row">
      <bs-checkbox-multiple
        v-for="tag in tags"
        :key="tag.id"
        :value="tag"
        :selected-values="ghost.tags"
      >
        <span class="badge bg-secondary">{{ tag.name }}</span>
        {{ tag.description }}
      </bs-checkbox-multiple>
    </div>
    <div class="row row-cols-auto">
      <bs-btn variant="success" small @click="saveGhost()">
        <span class="bi bi-save"></span> Save
      </bs-btn>
      <slot />
    </div>
  </div>
</template>

<style scoped></style>
