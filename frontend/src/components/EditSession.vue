<script lang="ts">
import { editSession, getSession } from "@/components/ApiService";
import { ISessionEditModel } from "@/components/ISessionEditModel";
import SessionEditor from "@/components/SessionEditor.vue";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import { defineComponent } from "vue";

export default defineComponent({
  components: { BsBtn, SessionEditor },
  data() {
    return {
      session: null as ISessionEditModel | null,
    };
  },
  async created(): Promise<void> {
    const session = (await getSession(this.$route.params.id as string)).session;
    if (session === null) {
      throw new Error("invalid session id");
    }
    this.session = { session: session, selectedTags: [] };
  },
  methods: {
    async updateSession(): Promise<void> {
      await editSession(this.session!.session.id, {
        description: this.session!.session.description,
        tags: this.session!.selectedTags,
        time: this.session!.session.time,
      });
      this.$router.back();
    },
  },
});
</script>

<template>
  <session-editor v-if="session !== null" v-model="session">
    <bs-btn variant="success" @click="updateSession()">
      <span class="bi bi-save" /> Save
    </bs-btn>
    <bs-btn variant="danger" @click="$router.back()">
      <span class="bi bi-x-square" /> Abort
    </bs-btn>
  </session-editor>
</template>

<style scoped></style>
