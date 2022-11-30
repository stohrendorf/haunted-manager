<script lang="ts">
import { getAnnouncements, IAnnouncementEntry } from "@/components/ApiService";
import { defineComponent } from "vue";

export default defineComponent({
  data() {
    return {
      announcements: [] as IAnnouncementEntry[],
    };
  },
  async created() {
    this.announcements = (await getAnnouncements()).announcements;
  },
});
</script>

<template>
  <div>
    <div
      v-for="(announcement, idx) in announcements"
      v-show="announcements"
      :key="idx"
      :class="
        'card bg-' +
        announcement.background_color +
        ' text-' +
        announcement.text_color
      "
    >
      <div class="card-body row justify-content-start">
        <i class="bi bi-info-square col col-auto" />
        <!-- eslint-disable-next-line -->
        <div class="col align-self-stretch" v-html="announcement.message" />
      </div>
    </div>
  </div>
</template>

<style scoped></style>
