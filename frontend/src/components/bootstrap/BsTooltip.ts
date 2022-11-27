import { Directive } from "vue";
import { Tooltip } from "bootstrap";

const BsTooltip: Directive<HTMLElement> = {
  beforeMount(el) {
    new Tooltip(el);
  },
};

export default BsTooltip;
