import ProfileView from "@/components/ProfileView.vue";
import { createPinia, setActivePinia } from "pinia";

describe("<NotVerifiedLock />", () => {
  it("shows a warning for anonymous users", () => {
    cy.intercept("GET", "/api/v0/auth/profile", {
      body: {
        authenticated: false,
        email: null,
        username: "anonymous",
        verified: false,
        auth_token: null,
      },
    });

    cy.mount(ProfileView, {
      global: {
        plugins: setActivePinia(createPinia()),
      },
    });

    cy.get(".alert-warning").should("have.length", 1).should("be.visible");
    cy.get("button").should("have.length", 3);
    cy.get("button.disabled").should("have.length", 1);
  });

  it("shows a warning for unverified users", () => {
    cy.intercept("GET", "/api/v0/auth/profile", {
      body: {
        authenticated: true,
        email: null,
        username: "anonymous",
        verified: false,
        auth_token: "token123",
      },
    });

    cy.mount(ProfileView, {
      global: {
        plugins: setActivePinia(createPinia()),
      },
    });

    cy.get(".alert-warning").should("have.length", 1).should("be.visible");
    cy.get("button").should("have.length", 3);
    cy.get("button.disabled").should("have.length", 1);
  });

  it("does not show a warning for verified users", () => {
    cy.intercept("GET", "/api/v0/auth/profile", {
      body: {
        authenticated: true,
        email: null,
        username: "anonymous",
        verified: true,
        auth_token: null,
      },
    });

    cy.mount(ProfileView, {
      global: {
        plugins: setActivePinia(createPinia()),
      },
    });

    cy.get(".alert-warning").should("have.length", 1).should("not.be.visible");
    cy.get("button").should("have.length", 3);
    cy.get("button.disabled").should("have.length", 1);
  });

  it("maps data to the controls", () => {
    cy.intercept("GET", "/api/v0/auth/profile", {
      body: {
        authenticated: true,
        email: "email@example.com",
        username: "username123",
        verified: true,
        auth_token: "token123",
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
    cy.get("button").should("have.length", 3);
    cy.get("button.disabled").should("have.length", 2);
  });
});
