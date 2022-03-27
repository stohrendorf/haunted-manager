<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { Prop } from "vue-property-decorator";
import { Modal } from "bootstrap";

@Options({})
export default class BsModal extends Vue {
  @Prop({ required: true })
  public title!: string;

  private _modal!: Modal;

  mounted() {
    this._modal = new Modal(this.$refs.modal as Element, {
      backdrop: "static",
      keyboard: false,
    });
  }

  public toggle() {
    this._modal.toggle();
  }

  public show() {
    this._modal.show();
  }
}
</script>

<template>
  <div
    ref="modal"
    class="modal fade"
    tabindex="-1"
    :aria-labelledby="$.uid + '--title'"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 :id="$.uid + '--title'" class="modal-title">{{ title }}</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <slot />
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary" data-bs-dismiss="modal">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
