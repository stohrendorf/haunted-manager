import { Tooltip } from "bootstrap";
import { Directive } from "vue";

const BsTooltip: Directive<HTMLElement> = {
  beforeMount(el) {
    new Tooltip(el);
  },
};

export default BsTooltip;
