<script lang="ts">
import { ISession, editSession, getSession } from "@/components/ApiService";
import SessionEditor from "@/components/SessionEditor.vue";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import { defineComponent } from "vue";

export default defineComponent({
  components: { BsBtn, SessionEditor },
  data() {
    return {
      session: null as ISession | null,
    };
  },
  async created(): Promise<void> {
    const session = (await getSession(this.$route.params.id as string)).session;
    if (session === null) {
      throw new Error("invalid session id");
    }
    this.session = session;
  },
  methods: {
    async updateSession(): Promise<void> {
      await editSession(this.session!.id, {
        description: this.session!.description,
        tags: this.session!.tags.map((tag) => tag.id),
        time: this.session!.time,
        private: this.session!.private,
      });
      this.$router.back();
    },
  },
});
</script>

<template>
  <session-editor v-if="session" v-model="session">
    <bs-btn variant="success" @click="updateSession()">
      <span class="bi bi-save" /> Save
    </bs-btn>
    <bs-btn variant="danger" @click="$router.back()">
      <span class="bi bi-x-square" /> Abort
    </bs-btn>
  </session-editor>
</template>

<style scoped></style>
