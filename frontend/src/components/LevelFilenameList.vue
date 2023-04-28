<script lang="ts">
import { PropType, defineComponent } from "vue";

export default defineComponent({
  props: {
    levels: {
      type: Array as PropType<string[][]>,
      required: true,
    },
    game: {
      type: String,
      required: true,
    },
  },
});
</script>

<template>
  <table class="table table-sm table-responsive">
    <caption>
      List of
      {{
        game
      }}
      level names and their corresponding filenames
    </caption>

    <thead>
      <tr>
        <th scope="col" class="w-auto">Level Name</th>
        <th scope="col" class="w-75">Filename</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="level in levels" :key="level[0]">
        <td>{{ level[1] }}</td>
        <td>
          <code>{{ level[0] }}</code>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<style scoped></style>
