<script lang="ts">
import { Options, Vue } from "vue-class-component";
import SiteAnnouncementsList from "@/components/SiteAnnouncementsList.vue";
import LoginWidget from "@/components/LoginWidget.vue";
import LogoutWidget from "@/components/LogoutWidget.vue";
import NotVerifiedLock from "@/components/NotVerifiedLock.vue";
import BsNavbar from "@/components/bootstrap/BsNavbar.vue";
import BsNavbarNav from "@/components/bootstrap/BsNavbarNav.vue";
import BsRouterNavItem from "@/components/bootstrap/BsRouterNavItem.vue";
import BsDropdownNavItem from "@/components/bootstrap/BsDropdownNavItem.vue";
import {
  getProfile,
  getServerInfo,
  IServerInfoResponse,
} from "@/components/ApiService";
import { profileStore } from "@/components/ProfileStore";
import BsModal from "@/components/bootstrap/BsModal.vue";
import ClipboardCopyable from "@/components/utilities/ClipboardCopyable.vue";

@Options({
  components: {
    ClipboardCopyable,
    BsModal,
    SiteAnnouncementsList,
    LoginWidget,
    LogoutWidget,
    NotVerifiedLock,
    BsNavbar,
    BsNavbarNav,
    BsRouterNavItem,
    BsDropdownNavItem,
  },
})
export default class App extends Vue {
  public profileInfo = profileStore();
  private err: Error | null = null;
  private info: string = "";
  private serverInfo: IServerInfoResponse = {
    total_sessions: 0,
    total_users: 0,
    coop_url: "",
  };

  async created(): Promise<void> {
    this.profileInfo.$state = await getProfile();
    this.serverInfo = await getServerInfo();
  }

  errorCaptured(err: Error, vm: Vue, info: string): boolean {
    this.err = err;
    this.info = info;
    console.error(err, info);
    if (this.$refs.errorModal) (this.$refs.errorModal as BsModal).show();
    return false;
  }
}
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
          v-show="profileInfo.authenticated"
          to="/create-session"
          :disabled="!profileInfo.verified"
        >
          <not-verified-lock />
          <span class="bi bi-plus-square-fill" />
          Create Session
        </bs-router-nav-item>
        <bs-dropdown-nav-item
          v-show="profileInfo.authenticated"
          min-width="20em"
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
      </bs-navbar-nav>
      <bs-navbar-nav ms="auto">
        <li class="navbar-text text-info">
          <span class="bi bi-info-circle" />
          Happily providing {{ serverInfo.total_sessions }} sessions for
          {{ serverInfo.total_users }} users.
        </li>
      </bs-navbar-nav>
      <bs-navbar-nav ms="auto">
        <bs-dropdown-nav-item v-show="profileInfo.authenticated" end="true">
          <template #toggle>
            <not-verified-lock />
            {{ profileInfo.username }}
          </template>
          <logout-widget />
        </bs-dropdown-nav-item>
        <bs-dropdown-nav-item v-show="!profileInfo.authenticated" end="true">
          <template #toggle> Login/Register </template>
          <login-widget />
        </bs-dropdown-nav-item>
      </bs-navbar-nav>
    </bs-navbar>

    <article class="container-fluid container-md">
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
