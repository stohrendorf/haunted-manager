<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { getAnnouncements, IAnnouncementEntry } from "@/components/ApiService";

@Options({})
export default class SiteAnnouncementsList extends Vue {
  public announcements: IAnnouncementEntry[] = [];

  async created(): Promise<void> {
    this.announcements = (await getAnnouncements()).announcements;
  }
}
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
      <div class="card-body">
        <i class="bi bi-info-square" />
        {{ announcement.message }}
      </div>
    </div>
  </div>
</template>

<style scoped></style>
