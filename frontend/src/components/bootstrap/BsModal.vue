<script lang="ts">
import { Modal } from "bootstrap";
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    title: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      modal: null as Modal | null,
    };
  },
  mounted() {
    this.modal = new Modal(this.$refs.modal as Element, {
      backdrop: "static",
      keyboard: false,
    });
  },
  methods: {
    toggle() {
      this.modal!.toggle();
    },
    show() {
      this.modal!.show();
    },
  },
});
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
