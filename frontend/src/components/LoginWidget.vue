<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { getProfile, login } from "@/components/ApiService";
import { profileStore } from "@/components/ProfileStore";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import FloatingSingleLineInput from "@/components/bootstrap/FloatingSingleLineInput.vue";

@Options({ components: { FloatingSingleLineInput, BsBtn } })
export default class LoginWidget extends Vue {
  public profileInfo = profileStore();

  async formSubmit() {
    await login({ username: this.username, password: this.password });
    this.username = "";
    this.password = "";

    this.profileInfo.$state = await getProfile();
  }

  private username: string = "";
  private password: string = "";
}
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
          label="Username or Email"
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
    <div class="form-group mb-3">
      <bs-btn
        class="w-100"
        variant="success"
        type="submit"
        :disabled="!username || !password"
        >Login</bs-btn
      >
    </div>
    <div class="form-group">
      <bs-btn class="w-100" variant="primary" @click="$router.push('/register')"
        >Register</bs-btn
      >
    </div>
  </form>
</template>

<style scoped></style>
