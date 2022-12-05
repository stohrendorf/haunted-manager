<script lang="ts">
import {
  IGhostFileResponseEntry,
  ITag,
  deleteGhost,
  downloadGhost,
  getGhosts,
} from "@/components/ApiService";
import { profileStore } from "@/components/ProfileStore";
import TagFilterSelector from "@/components/TagFilterSelector.vue";
import TagList from "@/components/TagList.vue";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import BsSelect from "@/components/bootstrap/BsSelect.vue";
import BsTooltip from "@/components/bootstrap/BsTooltip";
import { ISelectEntry } from "@/components/bootstrap/ISelectEntry";
import { seconds } from "@/components/filters";
import { getData, getFiles } from "@/components/utilities/untar";
import { defineComponent } from "vue";
import { XzReadableStream } from "xzwasm";

enum Ordering {
  Default,
  Reverse,
  DurationAsc,
  DurationDesc,
}

export default defineComponent({
  components: { BsSelect, TagList, TagFilterSelector, BsBtn },
  directives: { BsTooltip },
  data() {
    return {
      ghosts: [] as IGhostFileResponseEntry[],
      profile: profileStore(),
      tags: [] as ITag[],
      filterTags: [] as ITag[],
      levels: [] as ISelectEntry[],
      levelFilter: null as number | null,
      ordering: Ordering.Default as Ordering,
      orderingItems: [
        {
          value: Ordering.Default,
          title: "Newest First",
        },
        {
          value: Ordering.Reverse,
          title: "Oldest First",
        },
        {
          value: Ordering.DurationAsc,
          title: "Fastest First",
        },
        {
          value: Ordering.DurationDesc,
          title: "Longest First",
        },
      ] as ISelectEntry[],
    };
  },
  computed: {
    filteredGhosts() {
      let orderedGhosts = this.ghosts;
      if (this.filterTags.length !== 0) {
        orderedGhosts = this.ghosts.filter((ghost) =>
          this.filterTags.every((filterTag) =>
            ghost.tags.map((ghostTag) => ghostTag.id).includes(filterTag.id)
          )
        );
      }

      switch (this.ordering) {
        case Ordering.Default:
          break;
        case Ordering.Reverse:
          orderedGhosts.reverse();
          break;
        case Ordering.DurationAsc:
          orderedGhosts.sort((a, b) => (a.duration < b.duration ? -1 : 1));
          break;
        case Ordering.DurationDesc:
          orderedGhosts.sort((a, b) => (a.duration > b.duration ? -1 : 1));
          break;
      }

      return orderedGhosts;
    },
  },
  async created(): Promise<void> {
    this.ghosts = (await getGhosts()).files;
    const uniqueTags = new Map<number, ITag>();
    const uniqueLevels = new Map<number, ISelectEntry>();
    for (const ghost of this.ghosts) {
      for (const tag of ghost.tags) {
        uniqueTags.set(tag.id, tag);
      }
      uniqueLevels.set(ghost.level_id, {
        value: ghost.level_id,
        title: ghost.level_display,
      });
    }
    this.tags = [...uniqueTags.values()];
    this.tags.sort((a, b) => a.name.localeCompare(b.name));
    let levels = [...uniqueLevels.values()];
    levels.sort((a, b) => a.title.localeCompare(b.title));
    this.levels = [{ value: null, title: "No Level Filter" }, ...levels];
  },
  methods: {
    async deleteGhost(id: number): Promise<void> {
      await deleteGhost(id);
      this.ghosts = (await getGhosts()).files;
    },
    async downloadGhost(id: number): Promise<void> {
      const archive = await downloadGhost(id);
      if (archive === null) {
        return;
      }

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
    },

    seconds,
  },
});
</script>

<template>
  <div>
    <a ref="downloadAnchor" class="hiding" />
    <div class="input-group">
      <tag-filter-selector v-model="filterTags" :available-tags="tags" />
      <bs-select
        v-model="levelFilter"
        :items="levels"
        label="Level Filter"
        class="ms-1"
      />
      <bs-select
        v-model="ordering"
        :items="orderingItems"
        label="Ordering"
        class="ms-1"
      />
    </div>

    <div class="list-group mt-1">
      <div
        v-for="ghost in filteredGhosts"
        v-show="levelFilter === null || levelFilter === ghost.level_id"
        :key="ghost.id"
        class="list-group-item"
      >
        <tag-list :tags="ghost.tags" />
        <div>
          <a href="" @click.prevent="downloadGhost(ghost.id)">
            <strong>{{ ghost.level_display }}</strong>
          </a>
          &bull;
          <span class="bi bi-download"></span> {{ ghost.downloads }}
          &bull;
          {{ seconds(ghost.duration) }}
          &bull;
          {{ ghost.username }}
          &bull; Finish Type: {{ ghost.finish_type }}
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
