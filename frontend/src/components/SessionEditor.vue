<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { getTags, ISession, ITag } from "@/components/ApiService";
import BsBtn from "@/components/bootstrap/BsBtn.vue";
import FloatingSingleLineInput from "@/components/bootstrap/FloatingSingleLineInput.vue";
import BsCheckboxMultiple from "@/components/bootstrap/BsCheckboxMultiple.vue";
import { Prop } from "vue-property-decorator";
import DateTimePicker from "@/components/utilities/DateTimePicker.vue";
import moment from "moment";

@Options({
  components: {
    BsCheckboxMultiple,
    BsBtn,
    FloatingSingleLineInput,
    DateTimePicker,
  },
})
export default class SessionEditor extends Vue {
  private tags: ITag[] | null = null;
  get isEvent(): boolean {
    return this.session.time !== null;
  }
  set isEvent(value: boolean) {
    if (value === (this.session.time !== null)) return;
    if (value) {
      this.session.time = {
        start: moment().toISOString(),
        end: moment().toISOString(),
      };
    } else {
      this.session.time = null;
    }
  }

  @Prop({ required: true, default: () => ({ tags: [] }) })
  public session!: ISession;

  @Prop({ required: true, default: () => [] })
  private selectedTags!: number[];

  private updateSelectedTagsFromSession(): void {
    this.selectedTags.splice(0, this.selectedTags.length);
    this.selectedTags.push(
      ...this.session.tags.map(
        (sessionTag) =>
          this.tags!.filter((tag) => tag.name === sessionTag.name)[0].id
      )
    );
    this.$emit("update:selectedTags", this.selectedTags);
  }

  async created(): Promise<void> {
    this.tags = (await getTags()).tags;
    this.updateSelectedTagsFromSession();
    this.$watch(
      () => this.session,
      () => {
        this.updateSelectedTagsFromSession();
      },
      { deep: false }
    );
  }
}
</script>

<template>
  <form v-if="tags != null">
    <floating-single-line-input
      v-model="session.description"
      label="Description"
      required
    />

    <div class="card">
      <div class="card-body">
        <div class="card-title form-check form-check-inline">
          <input
            :id="'event-checkbox--' + $.uid"
            v-model="isEvent"
            class="form-check-input"
            type="checkbox"
          />
          <label :for="'event-checkbox--' + $.uid"> Scheduled Event </label>
        </div>
        <div v-if="session.time">
          <date-time-picker v-model="session.time.start">
            <strong> Start Time </strong>
            {{ $filters.datetime(session.time.start) }}
          </date-time-picker>
          <date-time-picker v-model="session.time.end">
            <strong> End Time </strong>
            {{ $filters.datetime(session.time.end) }}
          </date-time-picker>
          <small>All times are in your local time zone.</small>
        </div>
      </div>
    </div>

    <ul class="list-unstyled">
      <li v-for="tag in tags" :key="tag.id">
        <bs-checkbox-multiple :value="tag.id" :selected-values="selectedTags">
          <span class="badge bg-secondary">{{ tag.name }}</span>
          {{ tag.description }}
        </bs-checkbox-multiple>
      </li>
    </ul>
    <slot />
  </form>
</template>

<style scoped></style>
