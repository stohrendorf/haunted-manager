import RegisterAccount from "@/components/RegisterAccount.vue";

describe("<RegisterAccount />", () => {
  beforeEach(() => {
    cy.mount(RegisterAccount);
  });

  it("asks for data on initial display", () => {
    cy.get("div h3").should("have.text", "Register");
    cy.get("input[type=email]").should("not.have.value");
    cy.get("input[type=password]").should("not.have.value");
    cy.get("input[type=text]").should("not.have.value");
    cy.get("button").should("be.disabled");
  });

  it("is not submittable without email", () => {
    cy.get("input[type=password]").type("password");
    cy.get("input[type=text]").type("username");
    cy.get("button").should("be.disabled");
  });

  it("is not submittable without password", () => {
    cy.get("input[type=email]").type("test@example.com");
    cy.get("input[type=text]").type("username");
    cy.get("button").should("be.disabled");
  });

  it("is not submittable without username", () => {
    cy.get("input[type=password]").type("password");
    cy.get("input[type=text]").type("username");
    cy.get("button").should("be.disabled");
  });

  it("is not submittable with an invalid email", () => {
    cy.get("input[type=email]").type("bla");
    cy.get("input[type=password]").type("password");
    cy.get("input[type=text]").type("username");
    cy.get("button").should("be.disabled");
  });

  it("is submittable with valid inputs", () => {
    cy.get("input[type=email]").type("test@example.com");
    cy.get("input[type=password]").type("password");
    cy.get("input[type=text]").type("username");
    cy.get("button").should("not.be.disabled");
  });

  it("calls the endpoint with the correct values", () => {
    cy.intercept("POST", "/api/v0/auth/register", (req) => {
      expect(JSON.parse(req.body)).to.deep.eq({
        email: "test@example.com",
        password: "password",
        username: "username",
      });
      req.reply({
        success: true,
        message: "",
      });
    });

    cy.get("input[type=email]").type("test@example.com");
    cy.get("input[type=password]").type("password");
    cy.get("input[type=text]").type("username");
    cy.get("button").click();

    cy.get("div h3").should("have.text", "Registration Successful");
  });

  it("shows an error", () => {
    cy.intercept("POST", "/api/v0/auth/register", {
      success: false,
      message: "error message",
    });

    cy.get("input[type=email]").type("test@example.com");
    cy.get("input[type=password]").type("password");
    cy.get("input[type=text]").type("username");
    cy.get("button").click();

    cy.get("div h3").should("have.text", "Register");
    cy.get(".alert").should("have.text", "error message");
  });
});
