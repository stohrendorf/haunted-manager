import BsDropdownNavItem from "@/components/bootstrap/BsDropdownNavItem.vue";

describe("<BsDropdownNavItem />", () => {
  it("contains the message", () => {
    const msg = "test dropdown message";

    cy.mount(BsDropdownNavItem, {
      slots: {
        default: msg,
      },
    });

    cy.get("div.dropdown-menu")
      .should("have.text", msg)
      .should("have.attr", "style", "")
      .should("not.have.class", "dropdown-menu-end");
  });

  it("is positioned at the end", () => {
    cy.mount(BsDropdownNavItem, {
      props: {
        end: true,
      },
      slots: {
        default: "",
      },
    });

    cy.get("div.dropdown-menu")
      .should("have.attr", "style", "")
      .should("have.class", "dropdown-menu-end");
  });

  it("has a minimum width", () => {
    cy.mount(BsDropdownNavItem, {
      props: {
        minWidth: "12%",
      },
      slots: {
        default: "",
      },
    });

    cy.get("div.dropdown-menu")
      .should("have.attr", "style", "min-width: 12%;")
      .should("not.have.class", "dropdown-menu-end");
  });
});
