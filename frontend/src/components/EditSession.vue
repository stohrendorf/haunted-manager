<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { editSession, getSession, ISession } from "@/components/ApiService";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import SessionEditor from "@/components/SessionEditor.vue";

@Options({
  components: { BsBtn, SessionEditor },
})
export default class EditSession extends Vue {
  private session: ISession | null = null;
  private selectedTags: number[] = [];

  async created(): Promise<void> {
    const session = (await getSession(this.$route.params.id as string)).session;
    if (session === null) {
      throw new Error("invalid session id");
    }
    this.session = session;
    this.$emit("update:session");
  }

  async updateSession(): Promise<void> {
    await editSession(this.session!.id, {
      description: this.session!.description,
      tags: this.selectedTags,
    });
    this.$router.push("/");
  }
}
</script>

<template>
  <session-editor
    v-if="session !== null"
    :session="session"
    :selected-tags="selectedTags"
  >
    <bs-btn variant="success" @click="updateSession()">
      <span class="bi bi-save" /> Save
    </bs-btn>
    <bs-btn variant="danger" @click="$router.push('/')">
      <span class="bi bi-x-square" /> Abort
    </bs-btn>
  </session-editor>
</template>

<style scoped></style>
