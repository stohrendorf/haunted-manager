<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { IRegisterRequest, register } from "@/components/ApiService";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import BsAlert from "@/components/bootstrap/BsAlert.vue";

@Options({ components: { BsAlert, BsBtn } })
export default class RegisterAccount extends Vue {
  private readonly registrationInfo: IRegisterRequest = {
    email: "",
    password: "",
    username: "",
  };

  private error: string | null = null;

  async register(): Promise<void> {
    const result = await register(this.registrationInfo);
    if (!result.success) {
      this.error = result.message;
    } else {
      this.error = null;
    }
  }
}
</script>

<template>
  <div>
    <h3>Register</h3>

    <div class="input-group mb-3 disabled">
      <span class="input-group-text">Username</span>
      <input
        v-model="registrationInfo.username"
        type="text"
        class="form-control"
        placeholder="Username"
        aria-label="Username"
        required
      />
    </div>

    <div class="input-group mb-3 disabled">
      <span class="input-group-text">Email</span>
      <input
        v-model="registrationInfo.email"
        type="email"
        class="form-control"
        placeholder="Email"
        aria-label="Email"
        required
      />
    </div>

    <div class="input-group mb-3 disabled">
      <span class="input-group-text">Password</span>
      <input
        v-model="registrationInfo.password"
        type="password"
        class="form-control"
        placeholder="Password"
        aria-label="Password"
        required
      />
    </div>

    <bs-alert v-show="error" variant="danger">
      {{ error }}
    </bs-alert>

    <bs-btn
      variant="primary"
      :disabled="
        !registrationInfo.password ||
        !registrationInfo.email ||
        !registrationInfo.username
      "
      @click="register()"
    >
      Register
    </bs-btn>
  </div>
</template>

<style scoped></style>
