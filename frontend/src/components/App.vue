<script lang="ts">
import {
  IServerInfoResponse,
  getProfile,
  getServerInfo,
} from "@/components/ApiService";
import LoginWidget from "@/components/LoginWidget.vue";
import LogoutWidget from "@/components/LogoutWidget.vue";
import { profileStore } from "@/components/ProfileStore";
import SiteAnnouncementsList from "@/components/SiteAnnouncementsList.vue";
import BsDropdownNavItem from "@/components/bootstrap/BsDropdownNavItem.vue";
import BsModal from "@/components/bootstrap/BsModal.vue";
import BsNavbar from "@/components/bootstrap/BsNavbar.vue";
import BsNavbarNav from "@/components/bootstrap/BsNavbarNav.vue";
import BsRouterNavItem from "@/components/bootstrap/BsRouterNavItem.vue";
import ClipboardCopyable from "@/components/utilities/ClipboardCopyable.vue";
import { ComponentPublicInstance } from "@vue/runtime-core";
import { defineComponent } from "vue";

export default defineComponent({
  components: {
    ClipboardCopyable,
    BsModal,
    SiteAnnouncementsList,
    LoginWidget,
    LogoutWidget,
    BsNavbar,
    BsNavbarNav,
    BsRouterNavItem,
    BsDropdownNavItem,
  },
  data() {
    return {
      profileInfo: profileStore(),
      err: null as Error | null,
      info: "",
      serverInfo: {
        total_sessions: 0,
        total_users: 0,
        coop_url: "",
      } as IServerInfoResponse,
    };
  },
  async created(): Promise<void> {
    this.profileInfo.$state = await getProfile();
    this.serverInfo = await getServerInfo();
  },

  errorCaptured(
    err: unknown,
    vm: ComponentPublicInstance | null,
    info: string
  ): boolean {
    this.err = err as Error;
    this.info = info;
    console.error(err, info);
    if (this.$refs.errorModal) {
      (this.$refs.errorModal as typeof BsModal).show();
    }
    return false;
  },
});
</script>

<template>
  <div id="app">
    <bs-modal ref="errorModal" title="Oooops">
      Sorry, an error occured. Please come back again later.
      <hr />
      This is some warp drive internal error message, possibly useful to whoever
      messed this up:
      <code v-show="info" style="display: block" class="bg-dark mb-3">
        {{ info }}
      </code>
      <code style="display: block" class="bg-dark">
        Name: {{ err?.name }}<br />
        Message: {{ err?.message }}<br />
        Stack:<br />
        {{ err?.stack }}
      </code>
    </bs-modal>

    <bs-navbar variant="dark">
      <template #brand>
        <img src="../assets/logo.png" alt="Logo" style="height: 20px" />
        Haunted Server
      </template>

      <bs-navbar-nav>
        <bs-router-nav-item to="/">
          <span class="bi bi-list-ul" />
          Sessions
        </bs-router-nav-item>
        <bs-router-nav-item
          v-if="profileInfo.authenticated"
          to="/create-session"
        >
          <span class="bi bi-plus-square-fill" />
          Create Session
        </bs-router-nav-item>
        <bs-router-nav-item to="/ghosts">
          <span class="bi bi-list-ul" />
          Ghosts
        </bs-router-nav-item>
        <bs-router-nav-item
          v-if="profileInfo.authenticated"
          to="/upload-ghosts"
        >
          <span class="bi bi-upload" />
          Upload Ghosts
        </bs-router-nav-item>
      </bs-navbar-nav>
      <bs-navbar-nav ms="auto">
        <li class="navbar-text text-info">
          <span class="bi bi-bar-chart" />
          {{ serverInfo.total_users }} users,
          {{ serverInfo.total_sessions }} sessions,
          {{ serverInfo.total_ghosts }} ghosts,
          {{ $filters.seconds(serverInfo.total_ghost_duration) }}
          total ghost time
        </li>
      </bs-navbar-nav>
      <bs-navbar-nav ms="auto">
        <bs-dropdown-nav-item
          v-if="profileInfo.authenticated"
          min-width="20em"
          end
        >
          <template #toggle>
            <span class="bi bi-key-fill" /> Session Credentials
          </template>
          <div style="padding: 0.6666em">
            <div>
              The Server Address is
              <clipboard-copyable :value="serverInfo.coop_url">
                <code>{{ serverInfo.coop_url }}</code>
              </clipboard-copyable>
            </div>
            <hr />
            <div>
              Your Username is
              <clipboard-copyable :value="profileInfo.username">
                <code>{{ profileInfo.username }}</code>
              </clipboard-copyable>
            </div>
            <hr />
            <div>
              Your Personal Auth Token is
              <clipboard-copyable :value="profileInfo.auth_token">
                <code>{{ profileInfo.auth_token }}</code>
              </clipboard-copyable>
              <small class="text-secondary">
                You can re-generate this token in your profile if it gets
                compromised.
              </small>
            </div>
          </div>
        </bs-dropdown-nav-item>
        <bs-dropdown-nav-item v-if="profileInfo.authenticated" end>
          <template #toggle>
            {{ profileInfo.username }}
          </template>
          <logout-widget />
        </bs-dropdown-nav-item>
        <bs-dropdown-nav-item v-else end>
          <template #toggle> Login/Register</template>
          <login-widget />
        </bs-dropdown-nav-item>
      </bs-navbar-nav>
    </bs-navbar>

    <article class="container-fluid container-md pb-5 mb-5 mt-2">
      <site-announcements-list />
      <router-view />
    </article>

    <footer class="bg-dark text-light fixed-bottom">
      <div class="text-center" style="margin: 1em">
        This site only uses strictly necessary cookies. No ad cookies, no
        analytics cookies, no third-party cookies.
      </div>
    </footer>
  </div>
</template>

<style></style>
