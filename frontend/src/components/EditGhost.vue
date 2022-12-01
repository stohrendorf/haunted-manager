<script lang="ts">
import { IGhostFileResponseEntry, getGhost } from "@/components/ApiService";
import GhostEditor from "@/components/GhostEditor.vue";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import { defineComponent } from "vue";

export default defineComponent({
  components: { BsBtn, GhostEditor },
  data() {
    return {
      ghost: null as IGhostFileResponseEntry | null,
    };
  },
  async created(): Promise<void> {
    const ghost = (await getGhost(parseInt(this.$route.params.id as string)))
      .ghost;
    if (ghost === null) {
      throw new Error("invalid ghost id");
    }
    this.ghost = ghost;
  },
});
</script>

<template>
  <ghost-editor
    v-if="ghost !== null"
    v-model="ghost"
    :published="ghost.published"
    @saved="$router.back()"
  >
    <bs-btn variant="danger" @click="$router.back()">
      <span class="bi bi-x-square" /> Abort
    </bs-btn>
  </ghost-editor>
</template>

<style scoped></style>
