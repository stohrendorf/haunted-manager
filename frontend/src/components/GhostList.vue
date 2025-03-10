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
  DownloadsAsc,
  DownloadsDesc,
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
      finishTypes: [] as ISelectEntry[],
      finishTypeFilter: null as string | null,
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
        {
          value: Ordering.DownloadsAsc,
          title: "Least Downloads First",
        },
        {
          value: Ordering.DownloadsDesc,
          title: "Most Downloads First",
        },
      ] as ISelectEntry[],
    };
  },
  computed: {
    filteredGhosts() {
      let orderedGhosts = [...this.ghosts];
      if (this.filterTags.length !== 0) {
        orderedGhosts = this.ghosts.filter((ghost) =>
          this.filterTags.every((filterTag) =>
            ghost.tags.map((ghostTag) => ghostTag.id).includes(filterTag.id),
          ),
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
        case Ordering.DownloadsAsc:
          orderedGhosts.sort((a, b) => (a.downloads < b.downloads ? -1 : 1));
          break;
        case Ordering.DownloadsDesc:
          orderedGhosts.sort((a, b) => (a.downloads > b.downloads ? -1 : 1));
          break;
      }

      return orderedGhosts;
    },
  },
  async created(): Promise<void> {
    this.ghosts = (await getGhosts()).files;
    const uniqueTags = new Map<number, ITag>();
    const uniqueLevels = new Map<number, ISelectEntry>();
    const uniqueFinishTypes = [] as string[];
    for (const ghost of this.ghosts) {
      for (const tag of ghost.tags) {
        uniqueTags.set(tag.id, tag);
      }
      uniqueLevels.set(ghost.level_id, {
        value: ghost.level_id,
        title: ghost.level_display,
      });
      if (!uniqueFinishTypes.includes(ghost.finish_type)) {
        uniqueFinishTypes.push(ghost.finish_type);
      }
    }
    this.tags = [...uniqueTags.values()];
    this.tags.sort((a, b) => a.name.localeCompare(b.name));
    const levels = [...uniqueLevels.values()];
    levels.sort((a, b) => a.title.localeCompare(b.title));
    this.levels = [{ value: null, title: "No Level Filter" }, ...levels];
    uniqueFinishTypes.sort();
    this.finishTypes = [
      { value: null, title: "No Finish Type Filter" },
      ...uniqueFinishTypes.map((t) => ({
        value: t,
        title: t,
      })),
    ];
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
        e.name.toLowerCase().endsWith(".bin"),
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
        v-model="finishTypeFilter"
        :items="finishTypes"
        label="Finish Type Filter"
        class="ms-1"
      />
      <bs-select
        v-model="ordering"
        :items="orderingItems"
        label="Ordering"
        class="ms-1"
      />
    </div>

    <table class="table table-bordered table-hover">
      <thead>
        <tr>
          <th scope="col" class="fit">
            <span v-bs-tooltip class="bi bi-download" title="Downloads"></span>
          </th>
          <th scope="col" class="fit">Level</th>
          <th scope="col" class="fit">Duration</th>
          <th scope="col" class="fit">Tags</th>
          <th scope="col" class="fit">Finish Type</th>
          <th scope="col" class="fit">Uploader</th>
          <th scope="col">Description</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="ghost in filteredGhosts"
          v-show="
            (levelFilter === null || levelFilter === ghost.level_id) &&
            (finishTypeFilter === null ||
              finishTypeFilter === ghost.finish_type)
          "
          :key="ghost.id"
        >
          <td class="fit">
            {{ ghost.downloads }}
          </td>
          <td class="fit">
            <a href="" @click.prevent="downloadGhost(ghost.id)">
              {{ ghost.level_display }}
            </a>
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
          </td>
          <td class="fit">
            {{ seconds(ghost.duration) }}
          </td>
          <td class="fit">
            <tag-list :tags="ghost.tags" />
          </td>
          <td class="fit">
            {{ ghost.finish_type }}
          </td>
          <td class="fit">
            {{ ghost.username }}
          </td>
          <td>
            {{ ghost.description }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
td.fit,
th.fit {
  width: 0.1%;
  white-space: nowrap;
}
</style>
