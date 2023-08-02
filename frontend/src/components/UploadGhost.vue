<script lang="ts">
import {
  IGhostFileResponseEntry,
  IQuotaResponse,
  deleteGhost,
  getGhostsQuota,
  getStagingGhosts,
  uploadGhost,
} from "@/components/ApiService";
import GhostEditor from "@/components/GhostEditor.vue";
import BsAlert from "@/components/bootstrap/BsAlert.vue";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import ProgressBarSlice from "@/components/bootstrap/ProgressBarSlice.vue";
import { prettyBytes } from "@/components/filters";
import { defineComponent } from "vue";

export default defineComponent({
  components: {
    GhostEditor,
    ProgressBarSlice,
    BsAlert,
    BsBtn,
  },
  data() {
    return {
      errors: [] as string[],
      quota: { max: 0, current: 0 } as IQuotaResponse,
      quotaPercent: 0.0,
      stagingGhosts: [] as IGhostFileResponseEntry[],
      file: null as File | null,
    };
  },
  async mounted(): Promise<void> {
    await this.updateQuota();
  },
  methods: {
    async updateQuota(): Promise<void> {
      this.quota = await getGhostsQuota();
      this.quotaPercent = Math.round(
        (this.quota.current / this.quota.max) * 100,
      );
      await this.updateGhostList();
    },

    async onFileSelected(event: InputEvent): Promise<void> {
      const files = (event.target as HTMLInputElement).files;
      if (!files || files.length != 1) {
        this.file = null;
        return;
      }
      this.file = files[0];
    },

    async doUpload(): Promise<void> {
      if (this.file != null) {
        const result = await uploadGhost([this.file]);
        if (!result.success) {
          this.errors.push(result.message);
        }
      }
      this.file = null;
      await this.updateQuota();
    },

    selectFile(): void {
      (this.$refs.fileInput as HTMLInputElement).click();
    },

    dropFile(e: DragEvent): void {
      if (!e.dataTransfer) {
        return;
      }
      const droppedFiles = e.dataTransfer.files;
      if (!droppedFiles || droppedFiles.length != 1) {
        return;
      }
      this.file = droppedFiles[0];
    },

    async deleteGhost(id: number): Promise<void> {
      await deleteGhost(id);
      await this.updateGhostList();
    },

    async updateGhostList(): Promise<void> {
      this.stagingGhosts = (await getStagingGhosts()).files;
    },

    prettyBytes,
  },
});
</script>

<template>
  <div class="mb-3">
    <h3>Upload</h3>
    <div v-show="errors">
      <bs-alert v-for="(error, i) in errors" :key="i" variant="danger">
        <strong>Oops! An error occurred.</strong>
        {{ error }}
      </bs-alert>
    </div>
    <div class="progress bg-info" style="height: 2rem">
      <progress-bar-slice
        :percent="(quota.current / quota.max) * 100"
        :class="{
          'overflow-visible bg-success': quotaPercent < 80,
          'overflow-visible bg-warning':
            quotaPercent >= 80 && quotaPercent < 90,
          'overflow-visible bg-danger': quotaPercent >= 90,
        }"
      >
        <span class="text-black">
          Quota
          {{ prettyBytes(quota.current, true) }} of
          {{ prettyBytes(quota.max, true) }}
        </span>
      </progress-bar-slice>
    </div>
    <div class="list-group">
      <div
        v-cloak
        class="list-group-item border-primary bg-light"
        @drop.prevent="dropFile"
        @dragover.prevent
      >
        <a class="text-center btn w-100" @click="selectFile">
          <span v-show="!file">Select ghost or drop here</span>
          <span v-show="file">{{ file?.name }}</span></a
        >
      </div>
    </div>
    <input
      v-show="false"
      ref="fileInput"
      type="file"
      accept=".tar.xz"
      @change="onFileSelected"
    />
    <a
      class="btn w-100"
      :class="{ disabled: !file, 'btn-primary': file }"
      @click="doUpload()"
    >
      <i class="bi bi-upload" /> Upload
    </a>

    <h3 v-if="stagingGhosts">Unpublished Ghosts</h3>

    <div class="list-group">
      <div
        v-for="(ghost, index) in stagingGhosts"
        :key="ghost.id"
        class="list-group-item"
      >
        <ghost-editor v-model="stagingGhosts[index]" @saved="updateGhostList">
          <bs-btn variant="danger" small @click="deleteGhost(ghost.id)">
            <span class="bi bi-trash" /> Delete
          </bs-btn>
        </ghost-editor>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
