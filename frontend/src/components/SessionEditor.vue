<script lang="ts">
import { ISession, ITag, getTags } from "@/components/ApiService";
import BsCheckboxMultiple from "@/components/bootstrap/BsCheckboxMultiple.vue";
import FloatingSingleLineInput from "@/components/bootstrap/FloatingSingleLineInput.vue";
import DateTimePicker from "@/components/utilities/DateTimePicker.vue";
import moment from "moment";
import { PropType, defineComponent } from "vue";

export default defineComponent({
  components: {
    BsCheckboxMultiple,
    FloatingSingleLineInput,
    DateTimePicker,
  },
  props: {
    modelValue: {
      type: Object as PropType<ISession>,
      required: true,
    },
    selectedTags: {
      type: Object as PropType<number[]>,
      required: true,
    },
  },
  events: ["update:session"],
  data() {
    return {
      tags: null as ITag[] | null,
      localSession: null as ISession | null,
      localSelectedTags: [] as number[],
    };
  },
  computed: {
    isEvent: {
      get(): boolean {
        return this.localSession!.time !== null;
      },
      set(value: boolean) {
        if (value === (this.localSession!.time !== null)) return;
        if (value) {
          this.localSession!.time = {
            start: moment().toISOString(),
            end: moment().toISOString(),
          };
        } else {
          this.localSession!.time = null;
        }
        this.sessionUpdated();
      },
    },
  },
  async created(): Promise<void> {
    this.tags = (await getTags()).tags;
    this.localSession = { ...this.modelValue };
    this.$watch(
      () => this.modelValue,
      () => {
        this.localSession = { ...this.modelValue };
        this.updateSelectedTagsFromSession();
      }
    );
    this.localSelectedTags = [...this.selectedTags];
    this.$watch(
      () => this.selectedTags,
      () => {
        this.localSelectedTags = [...this.selectedTags];
        this.updateSelectedTagsFromSession();
      }
    );
    this.updateSelectedTagsFromSession();
  },
  methods: {
    updateSelectedTagsFromSession(): void {
      this.localSelectedTags.splice(0, this.localSelectedTags.length);
      this.localSelectedTags.push(
        ...this.localSession!.tags.map(
          (sessionTag) =>
            this.tags!.filter((tag) => tag.name === sessionTag.name)[0].id
        )
      );
      this.$emit("update:selectedTags", this.localSelectedTags);
    },
    sessionUpdated() {
      this.$emit("update:modelValue", this.localSession);
    },
  },
});
</script>

<template>
  <form v-if="tags != null">
    <floating-single-line-input
      v-model="localSession.description"
      label="Description"
      required
      @change="sessionUpdated()"
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
        <div v-if="localSession.time">
          <date-time-picker
            v-model="localSession.time.start"
            @change="sessionUpdated()"
          >
            <strong> Start Time </strong>
            {{ $filters.datetime(localSession.time.start) }}
          </date-time-picker>
          <date-time-picker
            v-model="localSession.time.end"
            @change="sessionUpdated()"
          >
            <strong> End Time </strong>
            {{ $filters.datetime(localSession.time.end) }}
          </date-time-picker>
          <small>All times are in your local time zone.</small>
        </div>
      </div>
    </div>

    <ul class="list-unstyled">
      <li v-for="tag in tags" :key="tag.id">
        <bs-checkbox-multiple
          v-model="localSelectedTags"
          :value="tag.id"
          @change="$emit('update:selectedTags', localSelectedTags)"
        >
          <span class="badge bg-secondary">{{ tag.name }}</span>
          {{ tag.description }}
        </bs-checkbox-multiple>
      </li>
    </ul>
    <slot />
  </form>
</template>

<style scoped></style>
