import BsAccordion from "@/components/bootstrap/BsAccordion.vue";
import BsAccordionItem from "@/components/bootstrap/BsAccordionItem.vue";
import { h } from "vue";

describe("<BsAccordion />", () => {
  it("contains a single item", () => {
    cy.mount(BsAccordion, {
      slots: {
        default: () =>
          h(
            BsAccordionItem,
            {
              expanded: true,
            },
            {
              header: () => "header",
              default: () => "content",
            }
          ),
      },
    });

    cy.get(".accordion-item").should("have.length", 1);
    cy.get(".accordion-header").should("contain.text", "header");
    cy.get(".accordion-body").should("contain.text", "content");
  });

  it("contains two items", () => {
    cy.mount(BsAccordion, {
      slots: {
        default: () => [
          h(
            BsAccordionItem,
            {
              expanded: true,
            },
            {
              header: () => "header 1",
              default: () => "content 1",
            }
          ),
          h(
            BsAccordionItem,
            {
              expanded: false,
            },
            {
              header: () => "header 2",
              default: () => "content 2",
            }
          ),
        ],
      },
    });

    cy.get(".accordion-item").should("have.length", 2);
    cy.get(".accordion-item .accordion-header")
      .eq(0)
      .should("contain.text", "header 1");
    cy.get(".accordion-item .accordion-body")
      .eq(0)
      .should("contain.text", "content 1");
    cy.get(".accordion-item .accordion-header")
      .eq(1)
      .should("contain.text", "header 2");
    cy.get(".accordion-item .accordion-body")
      .eq(1)
      .should("contain.text", "content 2");
  });
});
