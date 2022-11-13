<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { Prop } from "vue-property-decorator";

@Options({})
export default class BsCheckbox extends Vue {
  @Prop()
  public key: any | undefined;

  @Prop()
  public value!: any;

  @Prop({ default: () => [] })
  public selectedValues!: any[];

  private checked: boolean = false;

  created(): void {
    const updateChecked = () => {
      this.checked = this.selectedValues.includes(this.value) ?? false;
    };

    this.$watch(
      () => this.selectedValues,
      () => {
        updateChecked();
      }
    );
    this.$watch(
      () => this.value,
      () => {
        updateChecked();
      }
    );
    updateChecked();
  }

  changed(): void {
    const checked = (
      document.getElementById(String(this.$.uid)) as HTMLInputElement
    ).checked;
    if (checked && !this.selectedValues.includes(this.value))
      this.selectedValues.push(this.value);
    else if (!checked && this.selectedValues.includes(this.value))
      this.selectedValues.splice(this.selectedValues.indexOf(this.value), 1);
    else return;
    this.$emit("update:selectedValues", this.selectedValues);
  }
}
</script>

<template>
  <div :key="key" class="form-check form-check-inline">
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
