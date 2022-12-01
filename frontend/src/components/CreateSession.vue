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
      } as ISession,
      selectedTags: [] as number[],
    };
  },
  methods: {
    async createSession(): Promise<void> {
      await createSession({
        description: this.session.description,
        tags: this.selectedTags,
        time: this.session.time,
      });
      this.$router.push("/");
    },
  },
});
</script>

<template>
  <session-editor v-model="session" :selected-tags="selectedTags">
    <bs-btn variant="success" @click="createSession()">Create</bs-btn>
  </session-editor>
</template>

<style scoped></style>
