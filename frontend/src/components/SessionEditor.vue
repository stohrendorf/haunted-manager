<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { getTags, ISession, ITag } from "@/components/ApiService";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import FloatingSingleLineInput from "@/components/bootstrap/FloatingSingleLineInput.vue";
import BsCheckbox from "@/components/bootstrap/BsCheckbox.vue";
import { Prop } from "vue-property-decorator";

@Options({ components: { BsCheckbox, BsBtn, FloatingSingleLineInput } })
export default class SessionEditor extends Vue {
  private tags: ITag[] | null = null;

  @Prop({ required: true, default: { tags: [] } })
  public session!: ISession;

  @Prop({ required: true, default: () => [] })
  private selectedTags!: number[];

  private updateSelectedTagsFromSession(): void {
    this.selectedTags.splice(0, this.selectedTags.length);
    this.selectedTags.push(
      ...this.session.tags.map(
        (sessionTag) =>
          this.tags!.filter((tag) => tag.name === sessionTag.name)[0].id
      )
    );
    this.$emit("update:selectedTags", this.selectedTags);
  }

  async created(): Promise<void> {
    this.tags = (await getTags()).tags;
    this.updateSelectedTagsFromSession();
    this.$watch(
      () => this.session,
      () => {
        this.updateSelectedTagsFromSession();
      },
      { deep: false }
    );
  }
}
</script>

<template>
  <form v-if="tags != null">
    <floating-single-line-input
      v-model="session.description"
      label="Description"
      required
    />
    <ul class="list-unstyled">
      <li v-for="tag in tags" :key="tag.id">
        <bs-checkbox :value="tag.id" :selected-values="selectedTags">
          <span class="badge bg-secondary">{{ tag.name }}</span>
          {{ tag.description }}
        </bs-checkbox>
      </li>
    </ul>
    <slot />
  </form>
</template>

<style scoped></style>
