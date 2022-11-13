<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { createSession, ISession } from "@/components/ApiService";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import FloatingSingleLineInput from "@/components/bootstrap/FloatingSingleLineInput.vue";
import BsCheckbox from "@/components/bootstrap/BsCheckbox.vue";
import EditSession from "@/components/EditSession.vue";

@Options({
  components: { BsCheckbox, BsBtn, FloatingSingleLineInput, EditSession },
})
export default class CreateSession extends Vue {
  private session: ISession = {
    id: "",
    owner: "",
    description: "",
    tags: [],
    players: [],
  };
  private selectedTags: number[] = [];

  async createSession(): Promise<void> {
    await createSession({
      description: this.session.description,
      tags: this.selectedTags,
    });
    this.$router.push("/");
  }
}
</script>

<template>
  <edit-session :session="session" :selected-tags="selectedTags">
    <bs-btn variant="success" @click="createSession()">Create</bs-btn>
  </edit-session>
</template>

<style scoped></style>
