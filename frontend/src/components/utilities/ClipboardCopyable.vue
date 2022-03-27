<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { Prop } from "vue-property-decorator";
import BsBtn from "@/components/bootstrap/BsBtn.vue";

@Options({
  components: { BsBtn },
})
export default class ClipboardCopyable extends Vue {
  @Prop({ required: true })
  public value!: string;

  async copyToClipboard(): Promise<void> {
    await navigator.clipboard.writeText(this.value);
  }
}
</script>

<template>
  <span class="btn-">
    <slot />&hairsp;<bs-btn
      variant="primary"
      :small="true"
      @click="copyToClipboard()"
    >
      <span class="bi bi-clipboard" />
    </bs-btn>
  </span>
</template>

<style scoped></style>
