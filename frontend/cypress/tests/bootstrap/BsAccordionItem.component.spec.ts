import BsAccordionItem from "@/components/bootstrap/BsAccordionItem.vue";

describe("<BsAccordionItem />", () => {
  const headerStr = "test header";
  const contentStr = "test content";

  it("contains the message", () => {
    cy.mount(BsAccordionItem, {
      props: {
        expanded: true,
      },
      slots: {
        header: () => headerStr,
        default: () => contentStr,
      },
    });

    cy.get("h2.accordion-header button.accordion-button").should(
      "have.text",
      headerStr
    );
    cy.get("div.accordion-collapse div.accordion-body").should(
      "have.text",
      contentStr
    );
  });

  it("is collapsed", () => {
    cy.mount(BsAccordionItem, {
      props: {
        expanded: false,
      },
      slots: {
        header: () => headerStr,
        default: () => contentStr,
      },
    });

    cy.get("h2.accordion-header button.accordion-button").should(
      "have.attr",
      "aria-expanded",
      "false"
    );
    cy.get("div.accordion-collapse").should("not.have.class", "show");
  });

  it("is shown", () => {
    cy.mount(BsAccordionItem, {
      props: {
        expanded: true,
      },
      slots: {
        header: () => headerStr,
        default: () => contentStr,
      },
    });

    cy.get("h2.accordion-header button.accordion-button").should(
      "have.attr",
      "aria-expanded",
      "true"
    );
    cy.get("div.accordion-collapse").should("have.class", "show");
  });
});
