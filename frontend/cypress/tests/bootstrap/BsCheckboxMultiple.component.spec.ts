import BsCheckboxMultiple from "@/components/bootstrap/BsCheckboxMultiple.vue";

describe("<BsCheckboxMultiple />", () => {
  const msg = "test checkbox message";

  it("contains the message", () => {
    // see: https://test-utils.vuejs.org/guide/
    cy.mount(BsCheckboxMultiple, {
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
