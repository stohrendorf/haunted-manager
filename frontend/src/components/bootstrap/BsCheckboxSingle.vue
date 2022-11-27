<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";

@Options({})
export default class BsCheckboxSingle extends Vue {
  @Prop({ required: true })
  public modelValue!: boolean;

  private checked: boolean = false;

  created() {
    this.checked = this.modelValue;
  }

  @Watch("modelValue")
  private modelValueChanged(): void {
    this.checked = this.modelValue;
  }

  @Watch("checked")
  private isCheckedChanged(): void {
    this.$emit("update:modelValue", this.checked);
  }
}
</script>

<template>
  <div class="form-check form-check-inline">
    <input
      :id="$.uid"
      v-model="checked"
      class="form-check-input"
      type="checkbox"
    />
    <label :for="$.uid"><slot /></label>
  </div>
</template>

<style scoped></style>
