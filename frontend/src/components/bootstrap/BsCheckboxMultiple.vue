<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { Prop, Emit } from "vue-property-decorator";

@Options({})
export default class BsCheckboxMultiple extends Vue {
  @Prop({ default: true, required: false })
  public value!: any;

  @Prop({ default: () => [] })
  public selectedValues!: any[];

  private checked: boolean = false;

  created(): void {
    const updateChecked = () => {
      const value = JSON.stringify(this.value);
      this.checked = this.selectedValues.some(
        (x) => JSON.stringify(x) == value
      );
      this.onChecked();
    };

    this.$watch(() => this.selectedValues, updateChecked);
    this.$watch(() => this.value, updateChecked);
    updateChecked();
  }

  changed(): void {
    const checked = (
      document.getElementById(String(this.$.uid)) as HTMLInputElement
    ).checked;
    const value = JSON.stringify(this.value);
    if (checked && !this.selectedValues.some((x) => JSON.stringify(x) == value))
      this.selectedValues.push(this.value);
    else if (
      !checked &&
      this.selectedValues.some((x) => JSON.stringify(x) == value)
    )
      this.selectedValues.splice(
        this.selectedValues.findIndex((x) => JSON.stringify(x) == value),
        1
      );
    else return;
    this.$emit("update:selectedValues", this.selectedValues);
    this.checked = checked;
    this.onChecked();
  }

  @Emit()
  onChecked(): boolean {
    return this.checked;
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
      :value="value"
      @input="changed"
    />
    <label :for="$.uid"><slot /></label>
  </div>
</template>

<style scoped></style>
