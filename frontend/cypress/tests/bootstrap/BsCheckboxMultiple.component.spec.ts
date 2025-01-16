import BsCheckboxMultiple from "@/components/bootstrap/BsCheckboxMultiple.vue";

describe("<BsCheckboxMultiple />", () => {
  it("contains the message", () => {
    const msg = "test checkbox message";

    cy.mount(BsCheckboxMultiple, {
      props: {
        value: 123,
      },
      slots: {
        default: msg,
      },
    });

    cy.get("div").should("contain.text", msg);
    cy.get("input").should("have.class", "form-check-input");
  });

  it("propagates the selected values", () => {
    const component = cy.mount(BsCheckboxMultiple, {
      props: {
        value: 123,
        modelValue: [],
      },
      slots: {
        default: "label",
      },
    });

    cy.get("input").click();
    cy.get("input").should("be.checked");

    component.then(async (wrapper) => {
      await wrapper.component.$nextTick();
      expect(wrapper.wrapper.emitted("update:modelValue")[0][0]).to.deep.equal([
        123,
      ]);
    });
  });
});
