import LoginWidget from "@/components/LoginWidget.vue";
import { createPinia, setActivePinia } from "pinia";

describe("<LoginWidget />", () => {
  beforeEach(() => {
    cy.mount(LoginWidget, {
      global: {
        plugins: setActivePinia(createPinia()),
      },
    });

    cy.intercept("GET", "/api/v0/auth/profile", {
      body: {
        authenticated: true,
        email: "email@example.com",
        username: "username",
        verified: true,
        auth_token: "token123",
      },
    }).as("profileRequest");
  });

  it("cannot be submitted on initial load", () => {
    cy.get("input[type='text']").should("be.empty");
    cy.get("input[type='password']").should("be.empty");
    cy.get(".alert").should("not.be.visible");
    cy.get("button.btn-success").should("be.disabled");
    cy.get("button.btn-primary").should("not.be.disabled");
  });

  it("cannot be submitted without username", () => {
    cy.get("input[type='password']").type("password");
    cy.get(".alert").should("not.be.visible");
    cy.get("button.btn-success").should("be.disabled");
    cy.get("button.btn-primary").should("not.be.disabled");
  });

  it("cannot be submitted without password", () => {
    cy.get("input[type='text']").type("username");
    cy.get(".alert").should("not.be.visible");
    cy.get("button.btn-success").should("be.disabled");
    cy.get("button.btn-primary").should("not.be.disabled");
  });

  it("can be submitted with valid data", () => {
    cy.get("input[type='text']").type("username");
    cy.get("input[type='password']").type("password");
    cy.get(".alert").should("not.be.visible");
    cy.get("button.btn-success").should("not.be.disabled");
    cy.get("button.btn-primary").should("not.be.disabled");

    cy.intercept("POST", "/api/v0/auth/login", (rq) => {
      expect(JSON.parse(rq.body)).to.deep.eq({
        username: "username",
        password: "password",
      });
      rq.reply({
        success: true,
        message: "",
      });
    }).as("loginRequest");

    cy.get("button.btn-success").click();
    cy.wait("@loginRequest");
    cy.wait("@profileRequest");
    cy.get(".alert").should("not.be.visible");
  });

  it("shows an error", () => {
    cy.get("input[type='text']").type("username");
    cy.get("input[type='password']").type("password");
    cy.get(".alert").should("not.be.visible");
    cy.get("button.btn-success").should("not.be.disabled");
    cy.get("button.btn-primary").should("not.be.disabled");

    cy.intercept("POST", "/api/v0/auth/login", (rq) => {
      expect(JSON.parse(rq.body)).to.deep.eq({
        username: "username",
        password: "password",
      });
      rq.reply({
        success: false,
        message: "error message",
      });
    }).as("loginRequest");

    cy.get("button.btn-success").click();
    cy.wait("@loginRequest");
    cy.get(".alert").should("be.visible").should("have.text", "error message");
  });
});
