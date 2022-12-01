import ProgressBarSlice from "@/components/bootstrap/ProgressBarSlice.vue";

describe("<ProgressBarSlice />", () => {
  it("contains the message and width", () => {
    const msg = "test message";

    cy.mount(ProgressBarSlice, {
      props: {
        percent: 12,
      },
      slots: {
        default: msg,
      },
    });

    cy.get("div.progress-bar")
      .should("have.text", msg)
      .should("have.attr", "style", "width: 12%;");
  });
});
