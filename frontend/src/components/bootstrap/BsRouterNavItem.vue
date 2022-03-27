<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { Prop } from "vue-property-decorator";

@Options({})
export default class BsRouterNavItem extends Vue {
  @Prop({ required: true })
  public to!: string;

  @Prop({ required: false, default: false })
  public disabled!: boolean;
}
</script>

<template>
  <li class="nav-item">
    <router-link :to="to" class="nav-link" :class="{ disabled: disabled }">
      <slot />
    </router-link>
  </li>
</template>

<style scoped></style>
