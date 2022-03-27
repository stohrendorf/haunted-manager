<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { profileStore } from "@/components/ProfileStore";
import BsTooltip from "@/components/bootstrap/BsTooltip";

@Options({
  directives: { BsTooltip },
})
export default class NotVerifiedLock extends Vue {
  private profile = profileStore();
}
</script>

<template>
  <span v-bs-tooltip title="You haven't verified your email address yet.">
    <i v-show="profile.authenticated && !profile.verified" class="bi bi-lock" />
  </span>
</template>

<style scoped></style>
