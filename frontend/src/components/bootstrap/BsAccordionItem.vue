<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { Prop } from "vue-property-decorator";

@Options({})
export default class BsAccordionItem extends Vue {
  @Prop({ required: false, default: false })
  public expanded!: boolean;
}
</script>

<template>
  <div class="accordion-item">
    <h2 :id="$.uid" class="accordion-header">
      <button
        class="accordion-button"
        type="button"
        data-bs-toggle="collapse"
        :data-bs-target="'#' + $.uid + '--collapse'"
        :aria-expanded="expanded"
        :aria-controls="$.uid + '--collapse'"
      >
        <slot name="header" />
      </button>
    </h2>
    <div
      :id="$.uid + '--collapse'"
      :class="['accordion-collapse', 'collapse', expanded ? 'show' : '']"
      :aria-labelledby="$.uid"
      :data-bs-parent="'#' + $.parent.uid + '--container'"
    >
      <div class="accordion-body">
        <slot />
      </div>
    </div>
  </div>
</template>

<style scoped></style>
