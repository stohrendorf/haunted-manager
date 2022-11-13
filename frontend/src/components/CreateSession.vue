<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { createSession, ISession } from "@/components/ApiService";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import SessionEditor from "@/components/SessionEditor.vue";

@Options({
  components: { BsBtn, SessionEditor },
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
  <session-editor :session="session" :selected-tags="selectedTags">
    <bs-btn variant="success" @click="createSession()">Create</bs-btn>
  </session-editor>
</template>

<style scoped></style>
