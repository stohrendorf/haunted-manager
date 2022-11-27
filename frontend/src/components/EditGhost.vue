<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { getGhost, IGhostFileResponseEntry } from "@/components/ApiService";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import GhostEditor from "@/components/GhostEditor.vue";

@Options({
  components: { BsBtn, GhostEditor },
})
export default class EditGhost extends Vue {
  private ghost: IGhostFileResponseEntry | null = null;

  async created(): Promise<void> {
    const ghost = (await getGhost(parseInt(this.$route.params.id as string)))
      .ghost;
    if (ghost === null) {
      throw new Error("invalid ghost id");
    }
    this.ghost = ghost;
  }
}
</script>

<template>
  <ghost-editor
    v-if="ghost !== null"
    :ghost="ghost"
    :published="ghost.published"
    @saved="$router.back()"
  >
    <bs-btn variant="danger" @click="$router.back()">
      <span class="bi bi-x-square" /> Abort
    </bs-btn>
  </ghost-editor>
</template>

<style scoped></style>
