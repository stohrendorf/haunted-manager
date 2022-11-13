<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { getTags, ISession, ITag } from "@/components/ApiService";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import FloatingSingleLineInput from "@/components/bootstrap/FloatingSingleLineInput.vue";
import BsCheckbox from "@/components/bootstrap/BsCheckbox.vue";
import { Prop } from "vue-property-decorator";

@Options({ components: { BsCheckbox, BsBtn, FloatingSingleLineInput } })
export default class EditSession extends Vue {
  private tags: ITag[] = [];
  @Prop({ required: false, default: () => [] })
  private selectedTags!: number[];

  @Prop({ required: true })
  public session!: ISession;

  async created(): Promise<void> {
    this.tags = (await getTags()).tags;
    this.$watch(
      "session",
      () => {
        this.session.tags = this.tags.filter((tag) =>
          this.selectedTags.includes(tag.id)
        );
        this.$emit("update:session.tags");
      },
      { deep: true }
    );
  }
}
</script>

<template>
  <form>
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
