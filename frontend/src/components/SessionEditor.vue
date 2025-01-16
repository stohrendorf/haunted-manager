<script lang="ts">
import { ISession, ITag, getTags } from "@/components/ApiService";
import TagsSelector from "@/components/TagsSelector.vue";
import BsCheckboxSingle from "@/components/bootstrap/BsCheckboxSingle.vue";
import BsTooltip from "@/components/bootstrap/BsTooltip";
import FloatingSingleLineInput from "@/components/bootstrap/FloatingSingleLineInput.vue";
import { datetime } from "@/components/filters";
import DateTimePicker from "@/components/utilities/DateTimePicker.vue";
import moment from "moment";
import { PropType, defineComponent } from "vue";

export default defineComponent({
  components: {
    TagsSelector,
    BsCheckboxSingle,
    FloatingSingleLineInput,
    DateTimePicker,
  },
  directives: { BsTooltip },
  props: {
    modelValue: {
      type: Object as PropType<ISession>,
      required: true,
    },
  },
  emits: ["update:modelValue"],
  data() {
    return {
      tags: [] as ITag[],
      localSession: null as ISession | null,
    };
  },
  computed: {
    isEvent: {
      get(): boolean {
        return this.localSession!.time !== null;
      },
      set(value: boolean) {
        if (value === (this.localSession!.time !== null)) {
          return;
        }
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
    this.localSession = JSON.parse(JSON.stringify(this.modelValue));
    this.$watch(
      () => this.modelValue,
      () => {
        this.localSession = JSON.parse(JSON.stringify(this.modelValue));
      },
    );
  },
  methods: {
    sessionUpdated() {
      this.$emit("update:modelValue", this.localSession);
    },

    datetime,
  },
});
</script>

<template>
  <form v-if="tags != null && localSession">
    <floating-single-line-input
      v-model="localSession.description"
      label="Description"
      required
      @update:model-value="sessionUpdated()"
    />

    <div class="card">
      <div class="card-body">
        <div class="card-title form-check form-check-inline">
          <bs-checkbox-single
            v-model="localSession.private"
            @update:model-value="sessionUpdated()"
          >
            <span
              v-bs-tooltip
              title="This session will not be listed for others."
            >
              <span class="bi bi-eye-slash" /> Private
            </span>
          </bs-checkbox-single>
          <bs-checkbox-single
            v-model="isEvent"
            @update:model-value="sessionUpdated()"
          >
            Scheduled Event
          </bs-checkbox-single>
        </div>
        <div v-if="localSession.time !== null">
          <date-time-picker
            v-model="localSession.time.start"
            @update:model-value="sessionUpdated()"
          >
            <strong> Start Time </strong>
            {{ datetime(localSession.time.start) }}
          </date-time-picker>
          <date-time-picker
            v-model="localSession.time.end"
            @update:model-value="sessionUpdated()"
          >
            <strong> End Time </strong>
            {{ datetime(localSession.time.end) }}
          </date-time-picker>
          <small>All times are in your local time zone.</small>
        </div>
      </div>
    </div>

    <tags-selector
      v-model="localSession.tags"
      :available-tags="tags"
      @update:model-value="sessionUpdated()"
    />
    <slot />
  </form>
</template>

<style scoped></style>
