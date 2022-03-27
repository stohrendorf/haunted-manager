import SiteAnnouncementsList from "@/components/SiteAnnouncementsList.vue";

describe("<SiteAnnouncementsList />", () => {
  it("contains single alert", () => {
    cy.intercept("GET", "/api/v0/announcements", {
      body: {
        announcements: [
          {
            background_color: "danger",
            message: "some failure alert",
            text_color: "white",
          },
        ],
      },
    });

    cy.mount(SiteAnnouncementsList);

    cy.get("div.card")
      .should("have.length", 1)
      .should("have.class", "bg-danger")
      .should("have.class", "text-white");
  });

  it("contains two alerts", () => {
    cy.intercept("GET", "/api/v0/announcements", {
      body: {
        announcements: [
          {
            background_color: "danger",
            message: "some failure alert",
            text_color: "white",
          },
          {
            background_color: "success",
            message: "some success",
            text_color: "black",
          },
        ],
      },
    });

    cy.mount(SiteAnnouncementsList);

    cy.get("div.card").should("have.length", 2);
    cy.get("div.card")
      .eq(0)
      .should("have.class", "bg-danger")
      .should("have.class", "text-white")
      .should("contain.text", "some failure alert");
    cy.get("div.card")
      .eq(1)
      .should("have.class", "bg-success")
      .should("have.class", "text-black")
      .should("contain.text", "some success");
  });
});
