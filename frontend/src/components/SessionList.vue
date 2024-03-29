<script lang="ts">
import {
  ISession,
  ITag,
  getSessions,
  deleteSession as deleteSessionRequest,
} from "@/components/ApiService";
import { profileStore } from "@/components/ProfileStore";
import TagFilterSelector from "@/components/TagFilterSelector.vue";
import TagList from "@/components/TagList.vue";
import BsAlert from "@/components/bootstrap/BsAlert.vue";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import BsTooltip from "@/components/bootstrap/BsTooltip";
import { datetime } from "@/components/filters";
import ClipboardCopyable from "@/components/utilities/ClipboardCopyable.vue";
import { defineComponent } from "vue";

export default defineComponent({
  components: { ClipboardCopyable, BsAlert, BsBtn, TagFilterSelector, TagList },
  directives: { BsTooltip },
  data() {
    return {
      sessions: [] as ISession[],
      profile: profileStore(),
      filterTags: [] as ITag[],
      tags: [] as ITag[],
    };
  },
  computed: {
    filteredSessions() {
      if (this.filterTags.length === 0) {
        return this.sessions;
      }
      return this.sessions.filter((session) =>
        this.filterTags.every((filterTag) =>
          session.tags
            .map((sessionTag) => sessionTag.id)
            .includes(filterTag.id),
        ),
      );
    },
  },
  async created() {
    this.sessions = (await getSessions()).sessions;
    const uniqueTags = new Map<number, ITag>();
    for (const session of this.sessions) {
      for (const tag of session.tags) {
        uniqueTags.set(tag.id, tag);
      }
    }
    this.tags = [...uniqueTags.values()];
    this.tags.sort((a, b) => a.name.localeCompare(b.name));
  },
  methods: {
    async deleteSession(id: string): Promise<void> {
      await deleteSessionRequest(id);
      this.sessions = (await getSessions()).sessions;
    },

    datetime,
  },
});
</script>

<template>
  <div>
    <bs-alert v-if="!profile.authenticated" variant="primary">
      To join a session, you need to register.
    </bs-alert>
    <tag-filter-selector v-model="filterTags" :available-tags="tags" />
    <div class="list-group mt-1">
      <div
        v-for="session in filteredSessions"
        :key="session.id"
        class="list-group-item"
      >
        <div v-if="session.time !== null" class="row">
          <div class="col mb-2 rounded border-secondary border">
            <span class="bi bi-calendar3" /> Scheduled event, starting
            {{ datetime(session.time.start) }}, ending
            {{ datetime(session.time.end) }}.
            <small>All times are in your local time zone.</small>
          </div>
        </div>

        <div class="row">
          <div class="col col-4">
            <div class="row">
              <div class="col col-auto">
                <div class="row container justify-content-start">
                  <span v-if="session.private" class="col badge text-bg-info">
                    <span class="bi bi-eye-slash" /> Private Session
                  </span>
                  <span class="col text-secondary"
                    ><i class="fa-regular fa-user" /> {{ session.owner }}</span
                  >
                </div>
                <div class="row">
                  <clipboard-copyable :value="session.id">
                    <code>{{ session.id }}</code>
                  </clipboard-copyable>
                </div>
              </div>
            </div>

            <div
              v-if="
                profile.$state.username === session.owner ||
                profile.$state.is_staff
              "
              class="row mt-1"
            >
              <div class="col col-auto">
                <bs-btn
                  variant="danger"
                  small
                  @click="deleteSession(session.id)"
                >
                  <i class="bi bi-trash" /> Delete
                </bs-btn>
                <bs-btn
                  class="ms-1"
                  variant="primary"
                  small
                  @click="$router.push('/edit-session/' + session.id)"
                >
                  <i class="bi bi-pencil" /> Edit
                </bs-btn>
              </div>
            </div>
          </div>

          <div class="col col-8 justify-content-start">
            <div class="row">
              <tag-list
                v-if="session.tags && session.tags.length > 0"
                :tags="session.tags"
              />
            </div>

            <div v-if="session.description" class="row">
              <div>
                <i class="fa-regular fa-comment" />
                {{ session.description }}
              </div>
            </div>

            <div
              v-if="session.players && session.players.length > 0"
              class="row text-secondary"
            >
              <i class="fa fa-people-group" />{{ session.players.join(", ") }}.
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
