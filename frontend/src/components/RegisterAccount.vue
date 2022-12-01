<script lang="ts">
import { IRegisterRequest, register } from "@/components/ApiService";
import BsAlert from "@/components/bootstrap/BsAlert.vue";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import { defineComponent } from "vue";

export default defineComponent({
  components: { BsAlert, BsBtn },
  data() {
    return {
      registrationInfo: {
        email: "",
        password: "",
        username: "",
      } as IRegisterRequest,
      error: null as string | null,
      registrationSuccessful: false,
    };
  },
  methods: {
    async register(): Promise<void> {
      const result = await register(this.registrationInfo);
      if (!result.success) {
        this.error = result.message;
      } else {
        this.error = null;
        this.registrationSuccessful = true;
      }
    },
  },
});
</script>

<template>
  <div v-if="!registrationSuccessful">
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
        ref="email"
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
        !$refs.email.validity.valid ||
        !registrationInfo.username
      "
      @click="register()"
    >
      Register
    </bs-btn>
  </div>
  <div v-else>
    <h3>Registration Successful</h3>
    <bs-alert variant="primary">
      <p>Successfully registered</p>
      <p>Check your email to activate your account</p>
    </bs-alert>
  </div>
</template>

<style scoped></style>
