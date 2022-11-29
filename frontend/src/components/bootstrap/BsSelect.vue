<script lang="ts">
import { Vue } from "vue-class-component";
import { Emit, Prop } from "vue-property-decorator";
import { ISelectEntry } from "@/components/bootstrap/ISelectEntry";

export default class BsSelect extends Vue {
  @Prop({ default: false })
  public disabled!: boolean;
  @Prop({ required: true })
  public label!: string;
  @Prop({ required: true })
  public modelValue!: string;
  @Prop({ required: true })
  public items!: ISelectEntry[];

  private selectedValue: any = null;

  created() {
    this.selectedValue = this.modelValue;
  }

  @Emit("update:modelValue")
  updatedSelection(): any {
    return this.selectedValue;
  }
}
</script>

<template>
  <select
    v-model="selectedValue"
    class="form-select"
    :aria-label="label"
    :disabled="disabled"
    @change="updatedSelection()"
  >
    <option v-for="item in items" :key="item" :value="item.value">
      {{ item.title }}
    </option>
  </select>
</template>

<style scoped></style>
