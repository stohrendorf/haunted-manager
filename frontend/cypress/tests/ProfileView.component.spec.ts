import ProfileView from "@/components/ProfileView.vue";
import { createPinia, setActivePinia } from "pinia";

describe("<ProfileView />", () => {
  it("maps data to the controls", () => {
    cy.intercept("GET", "/api/v0/auth/profile", {
      body: {
        authenticated: true,
        email: "email@example.com",
        username: "username123",
        auth_token: "token123",
        is_staff: false,
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
    cy.get("button").should("have.length", 4);
    cy.get("button.disabled").should("have.length", 3);
  });

  it("enables the username button when changed", () => {
    cy.intercept("GET", "/api/v0/auth/profile", {
      body: {
        authenticated: true,
        email: "email@example.com",
        username: "username123",
        auth_token: "token123",
        is_staff: false,
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
    cy.get("button")
      .eq(0)
      .should("contain.text", "Change Username")
      .should("be.disabled");
    cy.get("input[aria-label='Username']").type("username456");
    cy.get("button").eq(0).should("not.be.disabled");
  });

  it("allows to change the username", () => {
    cy.intercept("GET", "/api/v0/auth/profile", {
      body: {
        authenticated: true,
        email: "email@example.com",
        username: "username123",
        auth_token: "token123",
        is_staff: false,
      },
    }).as("getProfile");

    cy.intercept("POST", "/api/v0/auth/change-username", (rq) => {
      expect(JSON.parse(rq.body)).to.deep.equal({ username: "username456" });
      rq.reply({ success: true, message: "" });
    }).as("changeUsername");

    cy.mount(ProfileView, {
      global: {
        plugins: setActivePinia(createPinia()),
      },
    });

    cy.get("input[aria-label='Username']")
      .should("have.length", 1)
      .should("have.value", "username123");
    cy.get("button")
      .eq(0)
      .should("contain.text", "Change Username")
      .should("be.disabled");
    cy.get("input[aria-label='Username']").clear().type("username456");
    cy.get("button").eq(0).should("not.be.disabled").click();
    cy.wait("@changeUsername");
    cy.wait("@getProfile");
    cy.get(".alert-danger").should("not.be.visible");
  });

  it("shows an error if username failed to change", () => {
    cy.intercept("GET", "/api/v0/auth/profile", {
      body: {
        authenticated: true,
        email: "email@example.com",
        username: "username123",
        auth_token: "token123",
        is_staff: false,
      },
    });

    cy.intercept("POST", "/api/v0/auth/change-username", (rq) => {
      expect(JSON.parse(rq.body)).to.deep.equal({ username: "username456" });
      rq.reply({ success: false, message: "error message" });
    }).as("changeUsername");

    cy.mount(ProfileView, {
      global: {
        plugins: setActivePinia(createPinia()),
      },
    });

    cy.get("input[aria-label='Username']")
      .should("have.length", 1)
      .should("have.value", "username123");
    cy.get("button")
      .eq(0)
      .should("contain.text", "Change Username")
      .should("be.disabled");
    cy.get("input[aria-label='Username']").clear().type("username456");
    cy.get("button").eq(0).should("not.be.disabled").click();
    cy.wait("@changeUsername");
    cy.get(".alert-danger")
      .should("be.visible")
      .should("have.text", "error message");
  });

  it("enables the email button when changed", () => {
    cy.intercept("GET", "/api/v0/auth/profile", {
      body: {
        authenticated: true,
        email: "email@example.com",
        username: "username123",
        auth_token: "token123",
        is_staff: false,
      },
    });

    cy.mount(ProfileView, {
      global: {
        plugins: setActivePinia(createPinia()),
      },
    });

    cy.get("input[aria-label='Email']")
      .should("have.length", 1)
      .should("have.value", "email@example.com");
    cy.get("button")
      .eq(2)
      .should("contain.text", "Change")
      .should("be.disabled");
    cy.get("input[aria-label='Email']").clear().type("other-email@example.com");
    cy.get("button").eq(2).should("not.be.disabled");
  });

  it("allows to change the email", () => {
    cy.intercept("GET", "/api/v0/auth/profile", {
      body: {
        authenticated: true,
        email: "email@example.com",
        username: "username123",
        auth_token: "token123",
        is_staff: false,
      },
    }).as("getProfile");

    cy.intercept("POST", "/api/v0/auth/change-email", (rq) => {
      expect(JSON.parse(rq.body)).to.deep.equal({
        email: "other-email@example.com",
      });
      rq.reply({ success: true, message: "" });
    }).as("changeEmail");

    cy.mount(ProfileView, {
      global: {
        plugins: setActivePinia(createPinia()),
      },
    });

    cy.get("input[aria-label='Email']")
      .should("have.length", 1)
      .should("have.value", "email@example.com");
    cy.get("button")
      .eq(2)
      .should("contain.text", "Change")
      .should("be.disabled");
    cy.get("input[aria-label='Email']").clear().type("other-email@example.com");
    cy.get("button").eq(2).should("not.be.disabled").click();
    cy.wait("@changeEmail");
    cy.wait("@getProfile");
    cy.get(".alert-danger").should("not.be.visible");
  });

  it("shows an error if email failed to change", () => {
    cy.intercept("GET", "/api/v0/auth/profile", {
      body: {
        authenticated: true,
        email: "email@example.com",
        username: "username123",
        auth_token: "token123",
        is_staff: false,
      },
    });

    cy.intercept("POST", "/api/v0/auth/change-email", (rq) => {
      expect(JSON.parse(rq.body)).to.deep.equal({
        email: "other-email@example.com",
      });
      rq.reply({ success: false, message: "error message" });
    }).as("changeEmail");

    cy.mount(ProfileView, {
      global: {
        plugins: setActivePinia(createPinia()),
      },
    });

    cy.get("input[aria-label='Email']")
      .should("have.length", 1)
      .should("have.value", "email@example.com");
    cy.get("button")
      .eq(2)
      .should("contain.text", "Change")
      .should("be.disabled");
    cy.get("input[aria-label='Email']").clear().type("other-email@example.com");
    cy.get("button").eq(2).should("not.be.disabled").click();
    cy.wait("@changeEmail");
    cy.get(".alert-danger")
      .should("be.visible")
      .should("have.text", "error message");
  });

  it("enables the password button when changed", () => {
    cy.intercept("GET", "/api/v0/auth/profile", {
      body: {
        authenticated: true,
        email: "email@example.com",
        username: "username123",
        auth_token: "token123",
        is_staff: false,
      },
    });

    cy.mount(ProfileView, {
      global: {
        plugins: setActivePinia(createPinia()),
      },
    });

    cy.get("input[aria-label='Password']")
      .should("have.length", 1)
      .should("not.have.value");
    cy.get("button")
      .eq(3)
      .should("contain.text", "Change Password")
      .should("be.disabled");
    cy.get("input[aria-label='Password']").clear().type("password123");
    cy.get("button").eq(3).should("not.be.disabled");
  });

  it("allows to change the password", () => {
    cy.intercept("GET", "/api/v0/auth/profile", {
      body: {
        authenticated: true,
        email: "email@example.com",
        username: "username123",
        auth_token: "token123",
        is_staff: false,
      },
    }).as("getProfile");

    cy.intercept("POST", "/api/v0/auth/change-password", (rq) => {
      expect(JSON.parse(rq.body)).to.deep.equal({
        password: "password123",
      });
      rq.reply({ success: true, message: "" });
    }).as("changePassword");

    cy.mount(ProfileView, {
      global: {
        plugins: setActivePinia(createPinia()),
      },
    });

    cy.get("input[aria-label='Password']").should("have.length", 1);
    cy.get("button")
      .eq(3)
      .should("contain.text", "Change Password")
      .should("be.disabled");
    cy.get("input[aria-label='Password']").clear().type("password123");
    cy.get("button").eq(3).should("not.be.disabled").click();
    cy.wait("@changePassword");
    cy.wait("@getProfile");
    cy.get(".alert-danger").should("not.be.visible");
  });

  it("shows an error if password failed to change", () => {
    cy.intercept("GET", "/api/v0/auth/profile", {
      body: {
        authenticated: true,
        email: "email@example.com",
        username: "username123",
        auth_token: "token123",
        is_staff: false,
      },
    });

    cy.intercept("POST", "/api/v0/auth/change-password", (rq) => {
      expect(JSON.parse(rq.body)).to.deep.equal({
        password: "password123",
      });
      rq.reply({ success: false, message: "error message" });
    }).as("changePassword");

    cy.mount(ProfileView, {
      global: {
        plugins: setActivePinia(createPinia()),
      },
    });

    cy.get("input[aria-label='Password']").should("have.length", 1);
    cy.get("button")
      .eq(3)
      .should("contain.text", "Change Password")
      .should("be.disabled");
    cy.get("input[aria-label='Password']").clear().type("password123");
    cy.get("button").eq(3).should("not.be.disabled").click();
    cy.wait("@changePassword");
    cy.get(".alert-danger")
      .should("be.visible")
      .should("have.text", "error message");
  });
});
