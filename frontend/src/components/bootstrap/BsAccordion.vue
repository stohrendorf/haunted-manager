<script lang="ts">
import { Options, Vue } from "vue-class-component";

@Options({})
export default class BsAccordion extends Vue {}
</script>

<template>
  <div :id="$.uid + '--container'" class="accordion">
    <slot />
  </div>
</template>

<style scoped></style>
