import BsSelect from "@/components/bootstrap/BsSelect.vue";
import type { ISelectEntry } from "@/components/bootstrap/ISelectEntry";

describe("<BsSelect />", () => {
  it("contains correct initial data", () => {
    const label = "test label";

    cy.mount(BsSelect, {
      props: {
        modelValue: "",
        label: label,
        items: [],
      },
    });

    cy.get("select").should("not.be.disabled");
    cy.get("option").should("have.length", 0);

    const testTitle = "test title";
    const testValue = "test value";

    cy.mount(BsSelect, {
      props: {
        modelValue: testValue,
        label: label,
        items: [
          {
            title: testTitle + "-other",
            value: testValue + "-other",
          },
          {
            title: testTitle,
            value: testValue,
          },
        ] as ISelectEntry[],
      },
    });

    cy.get("select").should("not.be.disabled").should("have.value", testValue);
    cy.get("option").should("have.length", 2);
    cy.get("option").eq(1).should("be.selected");
  });

  it("propagates selection changes", () => {
    const label = "test label";

    cy.mount(BsSelect, {
      props: {
        modelValue: "",
        label: label,
        items: [],
      },
    });

    cy.get("select").should("not.be.disabled");
    cy.get("option").should("have.length", 0);

    const testTitle = "test title";
    const testValue = "test value";

    const component = cy.mount(BsSelect, {
      props: {
        modelValue: testValue,
        label: label,
        items: [
          {
            title: testTitle + "-other",
            value: testValue + "-other",
          },
          {
            title: testTitle,
            value: testValue,
          },
        ] as ISelectEntry[],
      },
    });

    component.then(async (wrapper) => {
      await wrapper.component.$nextTick();
      expect(wrapper.component.selectedValue).to.equal(testValue);
    });

    const select = cy.get("select");
    select.should("not.be.disabled").should("have.value", testValue);
    select.select(0);
    cy.get("option").eq(0).should("be.selected");
    component.then(async (wrapper) => {
      await wrapper.component.$nextTick();
      expect(wrapper.wrapper.emitted("update:modelValue")[0][0]).to.not.equal(
        testValue,
      );
    });
  });
});
