import ProfileView from "@/components/ProfileView.vue";
import { createPinia, setActivePinia } from "pinia";

describe("<NotVerifiedLock />", () => {
  it("shows a warning for anonymous users", () => {
    cy.intercept("GET", "/auth/profile", {
      body: {
        authenticated: false,
        email: null,
        username: "anonymous",
        verified: false,
      },
    });

    cy.mount(ProfileView, {
      global: {
        plugins: setActivePinia(createPinia()),
      },
    });

    cy.get(".alert-warning").should("have.length", 1).should("be.visible");
    cy.get("button").should("have.length", 1).should("not.be.disabled");
  });

  it("shows a warning for unverified users", () => {
    cy.intercept("GET", "/auth/profile", {
      body: {
        authenticated: true,
        email: null,
        username: "anonymous",
        verified: false,
      },
    });

    cy.mount(ProfileView, {
      global: {
        plugins: setActivePinia(createPinia()),
      },
    });

    cy.get(".alert-warning").should("have.length", 1).should("be.visible");
    cy.get("button").should("have.length", 1).should("not.be.disabled");
  });

  it("does not show a warning for verified users", () => {
    cy.intercept("GET", "/auth/profile", {
      body: {
        authenticated: true,
        email: null,
        username: "anonymous",
        verified: true,
      },
    });

    cy.mount(ProfileView, {
      global: {
        plugins: setActivePinia(createPinia()),
      },
    });

    cy.get(".alert-warning").should("have.length", 1).should("not.be.visible");
    cy.get("button").should("have.length", 1).should("not.be.disabled");
  });

  it("maps data to the controls", () => {
    cy.intercept("GET", "/auth/profile", {
      body: {
        authenticated: true,
        email: "email@example.com",
        username: "username123",
        verified: true,
      },
    });

    cy.mount(ProfileView, {
      global: {
        plugins: setActivePinia(createPinia()),
      },
    });

    cy.get("input[aria-label='Username']")
      .should("have.length", 1)
      .should("have.value", "username123");
    cy.get("button").should("have.length", 1).should("be.disabled");
  });
});
