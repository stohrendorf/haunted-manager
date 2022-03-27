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
    await deleteSessionRequest({ session_id: id });
    this.sessions = (await getSessions()).sessions;
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
    <bs-alert v-show="profile.authenticated" variant="primary">
      Use your auth token
      <clipboard-copyable :value="profile.auth_token">
        <code>{{ profile.auth_token }}</code>
      </clipboard-copyable>
      to join a session.
    </bs-alert>
    <div class="list-group">
      <div
        v-for="session in sessions"
        :key="session.id"
        class="list-group-item"
      >
        <h5 class="mb-1">
          {{ session.id }}
          <small class="text-secondary"> by {{ session.owner }} </small>
          &nbsp;
          <small
            v-for="tag in session.tags"
            :key="tag.name"
            v-bs-tooltip
            :title="tag.description"
            class="badge bg-secondary"
          >
            {{ tag.name }}
          </small>
        </h5>

        <div v-show="session.description">
          {{ session.description }}
        </div>

        <clipboard-copyable :value="session.id" />
        <bs-btn
          v-show="profile.$state.username === session.owner"
          variant="danger"
          @click="deleteSession(session.id)"
        >
          <i class="bi bi-trash" /> Delete
        </bs-btn>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
