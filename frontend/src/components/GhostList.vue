<script lang="ts">
import { Options, Vue } from "vue-class-component";
import {
  getGhosts,
  IGhostFileResponseEntry,
  deleteGhost,
  downloadGhost,
} from "@/components/ApiService";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import BsTooltip from "@/components/bootstrap/BsTooltip";
import { profileStore } from "@/components/ProfileStore";
import { XzReadableStream } from "xzwasm";

import { getData, getFiles } from "@/components/utilities/untar";

@Options({
  components: { BsBtn },
  directives: { BsTooltip },
})
export default class GhostList extends Vue {
  private ghosts: IGhostFileResponseEntry[] = [];
  private profile = profileStore();

  async created(): Promise<void> {
    this.ghosts = (await getGhosts()).files;
  }

  async deleteGhost(id: number): Promise<void> {
    await deleteGhost(id);
    this.ghosts = (await getGhosts()).files;
  }
  async downloadGhost(id: number): Promise<void> {
    const archive = await downloadGhost(id);
    if (archive === null) return;

    const tarDataArray = [];
    for (const reader = new XzReadableStream(archive).getReader(); ; ) {
      const chunk = await reader.read();
      if (chunk.done) {
        break;
      }
      tarDataArray.push(...chunk.value);
    }
    const tarData = new Uint8Array(tarDataArray);
    const entries = getFiles(tarData).filter((e) =>
      e.name.toLowerCase().endsWith(".bin")
    );
    if (entries.length === 1) {
      const binData = getData(entries[0], tarData);
      const a = this.$refs.downloadAnchor as HTMLAnchorElement;
      const blob = new Blob([binData], { type: "application/octet-stream" });
      a.href = URL.createObjectURL(blob);
      a.download = entries[0].name;
      a.click();
    }
  }

  getGhostDownloadUrl(id: number): string {
    return `${process.env.VUE_APP_SERVER_URL}/api/v0/ghosts/${id}`;
  }
}
</script>

<template>
  <div>
    <a ref="downloadAnchor" class="hiding" />
    <div class="list-group">
      <div v-for="ghost in ghosts" :key="ghost.id" class="list-group-item">
        <div>
          <a href="" @click.prevent="downloadGhost(ghost.id)">
            <strong>{{ ghost.level_display }}</strong>
          </a>
          &bull;
          <span class="bi bi-download"></span> {{ ghost.downloads }}
          &bull;
          {{ $filters.seconds(ghost.duration) }}
          &bull;
          {{ ghost.username }}
          &bull; Finish Type: {{ ghost.finish_type }}
          <span v-if="ghost.tags">
            &bull;
            <span
              v-for="tag in ghost.tags"
              :key="tag.name"
              v-bs-tooltip
              :title="tag.description"
              class="badge bg-secondary"
            >
              {{ tag.name }}
            </span>
          </span>
        </div>
        <div v-if="ghost.description">
          {{ ghost.description }}
        </div>
        <div
          v-if="
            profile.$state.username === ghost.username ||
            profile.$state.is_staff
          "
          class="row mt-1"
        >
          <div class="col col-auto">
            <bs-btn variant="danger" small @click="deleteGhost(ghost.id)">
              <i class="bi bi-trash" /> Delete
            </bs-btn>
          </div>
          <div class="col col-auto">
            <bs-btn
              variant="primary"
              small
              @click="$router.push('/edit-ghost/' + ghost.id)"
            >
              <i class="bi bi-pencil" /> Edit
            </bs-btn>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
