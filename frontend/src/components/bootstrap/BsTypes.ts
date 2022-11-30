type Variant =
  | "primary"
  | "secondary"
  | "success"
  | "info"
  | "warning"
  | "danger"
  | "light"
  | "dark";

interface VariantConstructor {
  new (x: Variant): Variant;
}

export let Variant: VariantConstructor;

type Ms = "auto" | "5" | "4" | "3" | "2" | "1";

interface MsConstructor {
  new (x: Ms): Ms;
}

export let Ms: MsConstructor;
