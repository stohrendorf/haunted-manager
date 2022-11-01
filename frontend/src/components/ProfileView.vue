<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { getProfile, regenerateToken } from "@/components/ApiService";
import { profileStore } from "@/components/ProfileStore";
import SingleLineInput from "@/components/bootstrap/SingleLineInput.vue";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import BsAlert from "@/components/bootstrap/BsAlert.vue";

@Options({
  components: { BsAlert, SingleLineInput, BsBtn },
})
export default class ProfileView extends Vue {
  private profileInfo = profileStore();

  async created(): Promise<void> {
    this.profileInfo.$state = await getProfile();
  }

  async refreshToken(): Promise<void> {
    await regenerateToken();
    this.profileInfo.$state = await getProfile();
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

    <single-line-input
      v-model="profileInfo.username"
      label="Username"
      :disabled="true"
    />
    <single-line-input
      v-model="profileInfo.email"
      label="Email"
      type="email"
      required
    >
      <bs-btn
        :disabled="profileInfo.verified && profileInfo.email"
        outline
        variant="primary"
      >
        <span class="bi bi-check" /> Verify
      </bs-btn>
    </single-line-input>

    <single-line-input
      v-model="profileInfo.auth_token"
      label="Auth Token"
      type="text"
    >
      <bs-btn outline variant="primary" @click="refreshToken()">
        <span class="bi bi-arrow-repeat" /> Regenerate
      </bs-btn>
    </single-line-input>
  </div>
</template>

<style scoped></style>
