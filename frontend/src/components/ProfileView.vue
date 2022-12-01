<script lang="ts">
import {
  changeEmail,
  changePassword,
  changeUsername,
  getProfile,
  regenerateToken,
} from "@/components/ApiService";
import { profileStore } from "@/components/ProfileStore";
import BsAlert from "@/components/bootstrap/BsAlert.vue";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import FloatingSingleLineInput from "@/components/bootstrap/FloatingSingleLineInput.vue";
import { defineComponent } from "vue";

export default defineComponent({
  components: { BsAlert, FloatingSingleLineInput, BsBtn },
  data() {
    return {
      profileInfo: profileStore(),
      wantedEmail: "",
      wantedPassword: "",
      wantedUsername: "",
      err: "",
    };
  },
  async created(): Promise<void> {
    this.profileInfo.$state = await getProfile();
    this.wantedEmail = this.profileInfo.email ?? "";
    this.wantedUsername = this.profileInfo.username;
  },
  methods: {
    async refreshToken(): Promise<void> {
      await regenerateToken();
      this.profileInfo.$state = await getProfile();
      this.wantedEmail = this.profileInfo.email ?? "";
    },

    async changePassword(): Promise<void> {
      const response = await changePassword({ password: this.wantedPassword });
      if (response.success) this.err = "";
      else this.err = response.message;
    },

    async changeEmail(): Promise<void> {
      const response = await changeEmail({ email: this.wantedEmail });
      this.profileInfo.$state = await getProfile();
      if (response.success) this.err = "";
      else this.err = response.message;
    },

    async changeUsername(): Promise<void> {
      const response = await changeUsername({ username: this.wantedUsername });
      this.profileInfo.$state = await getProfile();
      if (response.success) this.err = "";
      else this.err = response.message;
    },
  },
});
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

    <floating-single-line-input v-model="wantedUsername" label="Username">
      <bs-btn
        :disabled="!wantedUsername || wantedUsername === profileInfo.username"
        variant="primary"
        @click="changeUsername()"
      >
        <span class="bi bi-person-badge" /> Change Username
      </bs-btn>
    </floating-single-line-input>

    <floating-single-line-input
      v-model="profileInfo.auth_token"
      label="Auth Token"
      type="text"
      disabled
    >
      <bs-btn variant="primary" @click="refreshToken()">
        <span class="bi bi-arrow-repeat" /> Regenerate
      </bs-btn>
    </floating-single-line-input>

    <floating-single-line-input
      v-model="wantedEmail"
      label="Email"
      type="email"
      required
    >
      <bs-btn
        :disabled="profileInfo.verified && profileInfo.email === wantedEmail"
        variant="primary"
        @click="changeEmail()"
      >
        <span class="bi bi-check" /> Change
      </bs-btn>
    </floating-single-line-input>

    <floating-single-line-input
      v-model="wantedPassword"
      label="Password"
      type="password"
    >
      <bs-btn
        :disabled="!wantedPassword"
        variant="primary"
        @click="changePassword()"
      >
        <span class="bi bi-key" /> Change Password
      </bs-btn>
    </floating-single-line-input>
  </div>
</template>

<style scoped></style>
