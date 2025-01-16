import { defineConfig } from "cypress";

export default defineConfig({
  component: {
    setupNodeEvents() {},
    specPattern: "cypress/tests/**/*.ts",
    devServer: {
      framework: "vue",
      bundler: "vite",
    },
  },

  e2e: {
    setupNodeEvents() {},
    specPattern: "cypress/e2e/**/*.ts",
  },
});
