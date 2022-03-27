import BsCheckbox from "@/components/bootstrap/BsCheckbox.vue";

describe("<BsCheckbox />", () => {
  const msg = "test checkbox message";

  it("contains the message", () => {
    // see: https://test-utils.vuejs.org/guide/
    cy.mount(BsCheckbox, {
      props: {
        value: 123,
      },
      slots: {
        default: msg,
      },
    });

    cy.get("div").should("contain.text", msg);
    cy.get("input")
      .should("have.attr", "value", 123)
      .should("have.class", "form-check-input");
  });
});
