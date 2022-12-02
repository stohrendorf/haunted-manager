<script lang="ts">
import { ITag, getTags } from "@/components/ApiService";
import { ISessionEditModel } from "@/components/ISessionEditModel";
import BsCheckboxMultiple from "@/components/bootstrap/BsCheckboxMultiple.vue";
import BsCheckboxSingle from "@/components/bootstrap/BsCheckboxSingle.vue";
import BsTooltip from "@/components/bootstrap/BsTooltip";
import FloatingSingleLineInput from "@/components/bootstrap/FloatingSingleLineInput.vue";
import DateTimePicker from "@/components/utilities/DateTimePicker.vue";
import moment from "moment";
import { PropType, defineComponent } from "vue";

export default defineComponent({
  components: {
    BsCheckboxSingle,
    BsCheckboxMultiple,
    FloatingSingleLineInput,
    DateTimePicker,
  },
  directives: { BsTooltip },
  props: {
    modelValue: {
      type: Object as PropType<ISessionEditModel>,
      required: true,
    },
  },
  events: ["update:session", "update:selectedTags"],
  data() {
    return {
      tags: null as ITag[] | null,
      localData: null as ISessionEditModel | null,
    };
  },
  computed: {
    isEvent: {
      get(): boolean {
        return this.localData!.session.time !== null;
      },
      set(value: boolean) {
        if (value === (this.localData!.session.time !== null)) {
          return;
        }
        if (value) {
          this.localData!.session.time = {
            start: moment().toISOString(),
            end: moment().toISOString(),
          };
        } else {
          this.localData!.session.time = null;
        }
        this.sessionUpdated();
      },
    },
  },
  async created(): Promise<void> {
    this.tags = (await getTags()).tags;
    this.localData = { ...this.modelValue };
    this.$watch(
      () => this.modelValue,
      () => {
        this.localData = { ...this.modelValue };
        this.updateSelectedTagsFromSession();
      }
    );
    this.updateSelectedTagsFromSession();
  },
  methods: {
    updateSelectedTagsFromSession(): void {
      this.localData!.selectedTags = this.localData!.session.tags.map(
        (sessionTag) =>
          this.tags!.filter((tag) => tag.name === sessionTag.name)[0].id
      );
      this.sessionUpdated();
    },
    sessionUpdated() {
      this.$emit("update:modelValue", this.localData);
    },
  },
});
</script>

<template>
  <form v-if="tags != null">
    <floating-single-line-input
      v-model="localData.session.description"
      label="Description"
      required
      @change="sessionUpdated()"
    />

    <div class="card">
      <div class="card-body">
        <div class="card-title form-check form-check-inline">
          <bs-checkbox-single
            v-model="localData.session.private"
            @change="sessionUpdated()"
          >
            <span
              v-bs-tooltip
              title="This session will not be listed for others."
            >
              <span class="bi bi-eye-slash" /> Private
            </span>
          </bs-checkbox-single>
          <bs-checkbox-single v-model="isEvent" @change="sessionUpdated()">
            Scheduled Event
          </bs-checkbox-single>
        </div>
        <div v-if="localData.session.time !== null">
          <date-time-picker
            v-model="localData.session.time.start"
            @change="sessionUpdated()"
          >
            <strong> Start Time </strong>
            {{ $filters.datetime(localData.session.time.start) }}
          </date-time-picker>
          <date-time-picker
            v-model="localData.session.time.end"
            @change="sessionUpdated()"
          >
            <strong> End Time </strong>
            {{ $filters.datetime(localData.session.time.end) }}
          </date-time-picker>
          <small>All times are in your local time zone.</small>
        </div>
      </div>
    </div>

    <ul class="list-unstyled">
      <li v-for="tag in tags" :key="tag.id">
        <bs-checkbox-multiple
          v-model="localData.selectedTags"
          :value="tag.id"
          @change="sessionUpdated"
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
