import BsAlert from "@/components/bootstrap/BsAlert.vue";

describe("<BsAlert />", () => {
  const msg = "test alert message";

  it("contains the message", () => {
    cy.mount(BsAlert, {
      props: {
        variant: "danger",
      },
      slots: {
        default: msg,
      },
    });

    cy.get("div.alert")
      .should("have.class", "alert")
      .should("have.class", "alert-danger")
      .should("have.text", msg);
  });
});
