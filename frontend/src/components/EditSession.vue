<script lang="ts">
import { Options, Vue } from "vue-class-component";
import {
  editSession,
  getSession,
  getTags,
  ITag,
} from "@/components/ApiService";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import SingleLineInput from "@/components/bootstrap/SingleLineInput.vue";
import BsCheckbox from "@/components/bootstrap/BsCheckbox.vue";

@Options({ components: { BsCheckbox, BsBtn, SingleLineInput } })
export default class EditSession extends Vue {
  private id: string = "";
  private tags: ITag[] = [];
  private description: string = "";
  private selectedTags: number[] = [];

  async created(): Promise<void> {
    this.tags = (await getTags()).tags;
    const response = await getSession(this.$route.params.id as String);
    this.description = response.session.description;
    this.id = response.session.id;
    for (const tag of response.session.tags) {
      const tagById = this.tags.find((t) => {
        return t.name == tag.name;
      });
      if (tagById !== undefined) this.selectedTags.push(tagById.id);
    }
  }

  async updateSession(): Promise<void> {
    let request = {
      id: this.id,
      description: this.description,
      tags: this.selectedTags,
    };
    await editSession(request);
    this.$router.push("/");
  }
}
</script>

<template>
  <form>
    <single-line-input v-model="description" label="Description" required />
    <ul class="list-unstyled">
      <li v-for="tag in tags" :key="tag.id">
        <input v-model="selectedTags" type="checkbox" :value="tag.id" />
        <label for="tag.id">
          <span class="badge bg-secondary">{{ tag.name }}</span>
          {{ tag.description }}
        </label>
      </li>
    </ul>
    <bs-btn variant="success" @click="updateSession()">Save</bs-btn>
  </form>
</template>
