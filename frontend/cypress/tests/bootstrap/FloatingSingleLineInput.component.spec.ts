import FloatingSingleLineInput from "@/components/bootstrap/FloatingSingleLineInput.vue";

describe("<FloatingSingleLineInput />", () => {
  it("contains correct initial data", () => {
    const msg = "test content";
    const label = "test label";
    const placeholder = "test placeholder";

    cy.mount(FloatingSingleLineInput, {
      props: {
        modelValue: msg,
        label: label,
        placeholder: placeholder,
      },
    });

    cy.get("input")
      .should("not.be.disabled")
      .should("have.attr", "type", "text")
      .should("not.have.attr", "required");
    cy.get("input").should("have.attr", "placeholder", placeholder);
    cy.get("input").should("have.value", msg);
    cy.get("label").should("have.text", label);
  });

  it("can be disabled", () => {
    cy.mount(FloatingSingleLineInput, {
      props: {
        modelValue: "value",
        label: "label",
        disabled: true,
      },
    });

    cy.get("input").should("be.disabled");
  });

  it("can be required", () => {
    cy.mount(FloatingSingleLineInput, {
      props: {
        modelValue: "value",
        label: "label",
        required: true,
      },
    });

    cy.get("input").should("have.attr", "required");
  });

  it("promoted the model value", () => {
    const component = cy.mount(FloatingSingleLineInput, {
      props: {
        modelValue: "value",
        label: "label",
        required: true,
      },
    });

    const testInput = "some new text";

    cy.get("input").clear().type(testInput);
    component.then(async (wrapper) => {
      await wrapper.component.$nextTick();
      expect(
        wrapper.wrapper.emitted("update:modelValue").reverse()[0][0],
      ).to.equal(testInput);
    });
  });
});
