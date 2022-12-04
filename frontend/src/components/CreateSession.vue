<script lang="ts">
import { ISession, createSession } from "@/components/ApiService";
import SessionEditor from "@/components/SessionEditor.vue";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import { defineComponent } from "vue";

export default defineComponent({
  components: { BsBtn, SessionEditor },
  data() {
    return {
      session: {
        id: "",
        owner: "",
        description: "",
        tags: [],
        players: [],
        time: null,
        private: false,
      } as ISession,
    };
  },
  methods: {
    async createSession(): Promise<void> {
      await createSession({
        description: this.session.description,
        tags: this.session.tags.map((tag) => tag.id),
        time: this.session.time,
        private: this.session.private,
      });
      this.$router.push("/");
    },
  },
});
</script>

<template>
  <session-editor v-model="session">
    <bs-btn variant="success" @click="createSession()">Create</bs-btn>
  </session-editor>
</template>

<style scoped></style>
