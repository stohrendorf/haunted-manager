import BsBtn from "@/components/bootstrap/BsBtn.vue";

describe("<BsBtn />", () => {
  it("contains the label", () => {
    const msg = "test label";

    cy.mount(BsBtn, {
      props: {
        variant: "danger",
      },
      slots: {
        default: msg,
      },
    });

    cy.get("button")
      .should("contain.text", msg)
      .should("have.class", "btn")
      .should("not.have.class", "small")
      .should("not.have.class", "disabled");
  });

  it("gets disabled", () => {
    cy.mount(BsBtn, {
      props: {
        variant: "danger",
      },
      attrs: {
        disabled: true,
      },
      slots: {
        default: "slot",
      },
    });

    cy.get("button")
      .should("have.class", "btn")
      .should("not.have.class", "small")
      .should("have.class", "disabled");
  });

  it("gets small", () => {
    cy.mount(BsBtn, {
      props: {
        variant: "danger",
      },
      attrs: {
        small: true,
      },
      slots: {
        default: "slot",
      },
    });

    cy.get("button")
      .should("have.class", "btn")
      .should("have.class", "smaller-button")
      .should("not.have.class", "disabled");
  });

  it("has variant class", () => {
    cy.mount(BsBtn, {
      props: {
        variant: "danger",
      },
      slots: {
        default: "slot",
      },
    });

    cy.get("button").should("have.class", "btn-danger");
  });

  it("has outline class", () => {
    cy.mount(BsBtn, {
      props: {
        variant: "danger",
      },
      slots: {
        default: "slot",
      },
    });

    cy.get("button")
      .should("not.have.class", "btn-outline-danger")
      .should("have.class", "btn-danger");

    cy.mount(BsBtn, {
      props: {
        variant: "danger",
      },
      attrs: {
        outline: true,
      },
      slots: {
        default: "slot",
      },
    });

    cy.get("button")
      .should("not.have.class", "btn-danger")
      .should("have.class", "btn-outline-danger");
  });
});
