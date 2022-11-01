<script lang="ts">
import { Options, Vue } from "vue-class-component";
import {
  changeEmail,
  changePassword,
  getProfile,
  regenerateToken,
} from "@/components/ApiService";
import { profileStore } from "@/components/ProfileStore";
import SingleLineInput from "@/components/bootstrap/SingleLineInput.vue";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import BsAlert from "@/components/bootstrap/BsAlert.vue";

@Options({
  components: { BsAlert, SingleLineInput, BsBtn },
})
export default class ProfileView extends Vue {
  private profileInfo = profileStore();
  private wantedEmail: string = "";
  private wantedPassword: string = "";
  private err: string = "";

  async created(): Promise<void> {
    this.profileInfo.$state = await getProfile();
    this.wantedEmail = this.profileInfo.email ?? "";
  }

  async refreshToken(): Promise<void> {
    await regenerateToken();
    this.profileInfo.$state = await getProfile();
    this.wantedEmail = this.profileInfo.email ?? "";
  }

  async changePassword(): Promise<void> {
    const response = await changePassword({ password: this.wantedPassword });
    if (response.success) this.err = "";
    else this.err = response.message;
  }

  async changeEmail(): Promise<void> {
    const response = await changeEmail({ email: this.wantedEmail });
    if (response.success) this.err = "";
    else this.err = response.message;
  }
}
</script>

<template>
  <div>
    <h3>Profile</h3>

    <bs-alert v-show="!profileInfo.verified" variant="warning">
      You haven't verified your email address yet. You are not allowed to create
      sessions.
    </bs-alert>

    <bs-alert v-show="err" variant="danger">
      <div v-for="(line, i) in err.split('\n')" :key="i">
        {{ line }}
      </div>
    </bs-alert>

    <single-line-input
      v-model="profileInfo.username"
      label="Username"
      disabled
    />

    <single-line-input
      v-model="profileInfo.auth_token"
      label="Auth Token"
      type="text"
      disabled
    >
      <bs-btn variant="primary" @click="refreshToken()">
        <span class="bi bi-arrow-repeat" /> Regenerate
      </bs-btn>
    </single-line-input>

    <single-line-input
      v-model="wantedEmail"
      label="Change Email"
      type="email"
      required
    >
      <bs-btn
        :disabled="profileInfo.verified && profileInfo.email === wantedEmail"
        variant="primary"
        @click="changeEmail()"
      >
        <span class="bi bi-check" /> Change &amp; Verify
      </bs-btn>
    </single-line-input>

    <single-line-input
      v-model="wantedPassword"
      label="Change Password"
      type="password"
    >
      <bs-btn
        :disabled="!wantedPassword"
        variant="primary"
        @click="changePassword()"
      >
        <span class="bi bi-key" /> Change Password
      </bs-btn>
    </single-line-input>
  </div>
</template>

<style scoped></style>
