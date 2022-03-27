<script lang="ts">
import { Options, Vue } from "vue-class-component";

@Options({})
export default class UnderConstruction extends Vue {}
</script>

<template>
  <div aria-hidden="true">
    <h2>
      <i class="bi bi-stop-circle" />
      This part is under construction.
    </h2>

    <p class="card-text placeholder-glow">
      <span class="placeholder col-7"></span>
      <span class="placeholder col-4"></span>
      <span class="placeholder col-4"></span>
      <span class="placeholder col-6"></span>
      <span class="placeholder col-8"></span>
    </p>
  </div>
</template>

<style scoped></style>
