<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { logout } from "@/components/ApiService";
import { profileStore } from "@/components/ProfileStore";
import BsBtn from "@/components/bootstrap/BsBtn.vue";

@Options({ components: { BsBtn } })
export default class LogoutWidget extends Vue {
  public profileInfo = profileStore();

  async logoutClicked(): Promise<void> {
    await logout();
    this.profileInfo.$state = {
      email: "",
      username: "",
      authenticated: false,
      verified: false,
      auth_token: null,
      is_staff: false,
    };
  }
}
</script>

<template>
  <div class="d-flex align-items-center px-8" style="padding: 0.6666em">
    <router-link to="/profile" class="flex-row btn btn-info">
      <span class="bi bi-person" /> Profile
    </router-link>
    <bs-btn variant="primary" @click="logoutClicked">
      <span class="bi bi-lock" /> Logout
    </bs-btn>
  </div>
</template>

<style scoped></style>
