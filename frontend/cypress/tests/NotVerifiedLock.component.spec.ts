import NotVerifiedLock from "@/components/NotVerifiedLock.vue";
import { createPinia, setActivePinia } from "pinia";
import { profileStore } from "@/components/ProfileStore";

describe("<NotVerifiedLock />", () => {
  beforeEach(() => {
    cy.mount(NotVerifiedLock, {
      global: {
        plugins: setActivePinia(createPinia()),
      },
    });
  });

  it("is invisible for anonymous users", () => {
    profileStore().$state.authenticated = false;
    cy.get("* i").should("not.be.visible");
  });

  it("is visible for anonymous users", () => {
    profileStore().$state.authenticated = true;
    cy.get("* i").should("be.visible");
  });

  it("is invisible for verified users", () => {
    profileStore().$state.authenticated = true;
    profileStore().$state.verified = true;
    cy.get("* i").should("not.be.visible");
  });
});
