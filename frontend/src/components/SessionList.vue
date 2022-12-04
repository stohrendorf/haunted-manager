<script lang="ts">
import { ISession, getSessions } from "@/components/ApiService";
import { deleteSession as deleteSessionRequest } from "@/components/ApiService";
import { profileStore } from "@/components/ProfileStore";
import BsAlert from "@/components/bootstrap/BsAlert.vue";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import BsTooltip from "@/components/bootstrap/BsTooltip";
import ClipboardCopyable from "@/components/utilities/ClipboardCopyable.vue";
import { defineComponent } from "vue";

export default defineComponent({
  components: { ClipboardCopyable, BsAlert, BsBtn },
  directives: { BsTooltip },
  data() {
    return {
      sessions: [] as ISession[],
      profile: profileStore(),
    };
  },
  async created() {
    this.sessions = (await getSessions()).sessions;
  },
  methods: {
    async deleteSession(id: string): Promise<void> {
      await deleteSessionRequest(id);
      this.sessions = (await getSessions()).sessions;
    },
  },
});
</script>

<template>
  <div>
    <bs-alert v-show="!profile.authenticated" variant="primary">
      To join a session, you need to register.
    </bs-alert>
    <div class="list-group">
      <div
        v-for="session in sessions"
        :key="session.id"
        class="list-group-item"
      >
        <div v-if="session.time !== null" class="row">
          <div class="col mb-2 rounded border-secondary border">
            <span class="bi bi-calendar3" /> Scheduled event, starting
            {{ $filters.datetime(session.time.start) }}, ending
            {{ $filters.datetime(session.time.end) }}.
            <small>All times are in your local time zone.</small>
          </div>
        </div>

        <div v-if="session.tags || session.private" class="row">
          <div class="col">
            <span v-if="session.private">
              <span class="bi bi-eye-slash" /> Private
            </span>

            <span
              v-for="tag in session.tags"
              :key="tag.name"
              v-bs-tooltip
              :title="tag.description"
              class="badge bg-secondary me-1"
            >
              {{ tag.name }}
            </span>
          </div>
        </div>

        <div v-if="session.description" class="row">
          <div>
            {{ session.description }}
          </div>
        </div>

        <div class="row text-secondary">
          <div v-if="session.players && session.players.length > 0">
            Currently playing: {{ session.players.join(", ") }}.
          </div>
          <div v-else>
            No active players in this session
            <span class="bi bi-emoji-frown" />
          </div>
        </div>

        <div class="row">
          <div class="col col-auto">
            <div class="row">
              <div>
                <clipboard-copyable :value="session.id">
                  <code>{{ session.id }}</code>
                </clipboard-copyable>
                <span class="text-secondary"> by {{ session.owner }}</span>
              </div>
            </div>
          </div>
        </div>

        <div
          v-if="
            profile.$state.username === session.owner || profile.$state.is_staff
          "
          class="row mt-1"
        >
          <div class="col col-auto">
            <bs-btn variant="danger" small @click="deleteSession(session.id)">
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
    </div>
  </div>
</template>

<style scoped></style>
