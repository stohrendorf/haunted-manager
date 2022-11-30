<script lang="ts">
import { getProfile, login } from "@/components/ApiService";
import { profileStore } from "@/components/ProfileStore";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import FloatingSingleLineInput from "@/components/bootstrap/FloatingSingleLineInput.vue";
import BsAlert from "@/components/bootstrap/BsAlert.vue";
import { defineComponent } from "vue";

export default defineComponent({
  components: { BsAlert, FloatingSingleLineInput, BsBtn },
  data() {
    return {
      profileInfo: profileStore(),
      username: "",
      password: "",
      loginError: "",
    };
  },
  methods: {
    async formSubmit() {
      const loginResult = await login({
        username: this.username.trim(),
        password: this.password,
      });
      if (!loginResult.success) {
        this.loginError = loginResult.message;
        return;
      }

      this.username = "";
      this.password = "";
      this.loginError = "";

      this.profileInfo.$state = await getProfile();
    },
  },
});
</script>

<template>
  <form
    class="px-8"
    style="padding: 0.6666em"
    @submit.prevent.stop="formSubmit()"
  >
    <div class="mb-3 row">
      <div class="col">
        <floating-single-line-input
          v-model="username"
          type="text"
          required
          label="Username"
        />
      </div>
    </div>
    <div class="mb-3 row">
      <div class="col">
        <floating-single-line-input
          v-model="password"
          type="password"
          required
          label="Password"
        />
      </div>
    </div>
    <div v-show="loginError" class="mb-3 row">
      <div class="col">
        <bs-alert variant="danger">{{ loginError }}</bs-alert>
      </div>
    </div>
    <div class="form-group mb-3">
      <bs-btn
        class="w-100"
        variant="success"
        type="submit"
        :disabled="!username || !password"
      >
        Login
      </bs-btn>
    </div>
    <div class="form-group">
      <bs-btn
        class="w-100"
        variant="primary"
        @click="$router.push('/register')"
      >
        Register
      </bs-btn>
    </div>
  </form>
</template>

<style scoped></style>
