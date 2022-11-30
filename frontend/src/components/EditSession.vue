<script lang="ts">
import { editSession, getSession, ISession } from "@/components/ApiService";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import SessionEditor from "@/components/SessionEditor.vue";
import { defineComponent } from "vue";

export default defineComponent({
  components: { BsBtn, SessionEditor },
  data() {
    return {
      session: null as ISession | null,
      selectedTags: [] as number[],
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
        tags: this.selectedTags,
        time: this.session!.time,
      });
      this.$router.back();
    },
  },
});
</script>

<template>
  <session-editor
    v-if="session !== null"
    v-model="session"
    :selected-tags="selectedTags"
  >
    <bs-btn variant="success" @click="updateSession()">
      <span class="bi bi-save" /> Save
    </bs-btn>
    <bs-btn variant="danger" @click="$router.back()">
      <span class="bi bi-x-square" /> Abort
    </bs-btn>
  </session-editor>
</template>

<style scoped></style>
