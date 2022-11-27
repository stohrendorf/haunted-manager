<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { Prop } from "vue-property-decorator";

@Options({})
export default class ProgressBarSlice extends Vue {
  @Prop({ required: true })
  public percent: number = 0;
}
</script>

<template>
  <div
    class="progress-bar"
    role="progressbar"
    :style="'width: ' + percent + '%'"
  >
    <slot />
  </div>
</template>

<style scoped></style>
