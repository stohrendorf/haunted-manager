<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { createSession, getTags, ITag } from "@/components/ApiService";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import SingleLineInput from "@/components/bootstrap/SingleLineInput.vue";
import BsCheckbox from "@/components/bootstrap/BsCheckbox.vue";

@Options({ components: { BsCheckbox, BsBtn, SingleLineInput } })
export default class CreateSession extends Vue {
  private tags: ITag[] = [];
  private description: string = "";
  private selectedTags: number[] = [];

  async created(): Promise<void> {
    this.tags = (await getTags()).tags;
  }

  async createSession(): Promise<void> {
    await createSession({
      description: this.description,
      tags: this.selectedTags,
    });
    this.$router.push("/");
  }
}
</script>

<template>
  <form>
    <single-line-input v-model="description" label="Description" required />
    <ul class="list-unstyled">
      <li v-for="tag in tags" :key="tag.id">
        <bs-checkbox :value="tag.id" :selected-values="selectedTags">
          <span class="badge bg-secondary">{{ tag.name }}</span>
          {{ tag.description }}
        </bs-checkbox>
      </li>
    </ul>
    <bs-btn variant="success" @click="createSession()">Create</bs-btn>
  </form>
</template>

<style scoped></style>
