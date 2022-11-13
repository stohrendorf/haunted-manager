<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { editSession, getSession, ISession } from "@/components/ApiService";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import SessionEditor from "@/components/SessionEditor.vue";

@Options({
  components: { BsBtn, SessionEditor },
})
export default class EditSession extends Vue {
  private session: ISession = {
    description: "",
    id: "",
    owner: "",
    players: [],
    tags: [],
  };
  private selectedTags: number[] = [];

  async beforeCreate(): Promise<void> {
    const session = (await getSession(this.$route.params.id as string)).session;
    if (session === null) {
      throw new Error("invalid session id");
    }
    this.session = session;
  }

  async updateSession(): Promise<void> {
    let request = {
      description: this.session.description,
      tags: this.selectedTags,
    };
    await editSession(this.session.id, request);
    this.$router.push("/");
  }
}
</script>

<template>
  <session-editor :session="session" :selected-tags="selectedTags">
    <bs-btn variant="success" @click="updateSession()"
      ><span class="bi bi-save" /> Save</bs-btn
    >
    <bs-btn variant="danger" @click="$router.push('/')"
      ><span class="bi bi-x-square" /> Abort</bs-btn
    >
  </session-editor>
</template>

<style scoped></style>
