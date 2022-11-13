<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { getSessions, ISession } from "@/components/ApiService";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import BsTooltip from "@/components/bootstrap/BsTooltip";
import { deleteSession as deleteSessionRequest } from "@/components/ApiService";
import { profileStore } from "@/components/ProfileStore";
import BsAlert from "@/components/bootstrap/BsAlert.vue";
import ClipboardCopyable from "@/components/utilities/ClipboardCopyable.vue";

@Options({
  components: { ClipboardCopyable, BsAlert, BsBtn },
  directives: { BsTooltip },
})
export default class SessionList extends Vue {
  private sessions: ISession[] = [];
  private profile = profileStore();

  async created(): Promise<void> {
    this.sessions = (await getSessions()).sessions;
  }

  async deleteSession(id: string): Promise<void> {
    await deleteSessionRequest(id);
    this.sessions = (await getSessions()).sessions;
  }

  editSession(id: String): void {
    this.$router.push("/edit-session/" + id);
  }
}
</script>

<template>
  <div>
    <bs-alert v-show="!profile.authenticated" variant="primary">
      To join a session, you need to register.
    </bs-alert>
    <bs-alert
      v-show="profile.authenticated && !profile.verified"
      variant="primary"
    >
      To create a session, you need to verify your email address.
    </bs-alert>
    <div class="list-group">
      <div
        v-for="session in sessions"
        :key="session.id"
        class="list-group-item"
      >
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
            <div class="row">
              <div>
                <span
                  v-for="tag in session.tags"
                  :key="tag.name"
                  v-bs-tooltip
                  :title="tag.description"
                  class="badge bg-secondary"
                >
                  {{ tag.name }}
                </span>
              </div>
            </div>
          </div>

          <div class="col">
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
          </div>
        </div>

        <div v-if="profile.$state.username === session.owner" class="row mt-1">
          <div class="col col-auto">
            <bs-btn variant="danger" small @click="deleteSession(session.id)">
              <i class="bi bi-trash" /> Delete
            </bs-btn>
          </div>
          <div class="col col-auto">
            <bs-btn variant="primary" small @click="editSession(session.id)">
              <i class="bi bi-pencil" /> Edit
            </bs-btn>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
