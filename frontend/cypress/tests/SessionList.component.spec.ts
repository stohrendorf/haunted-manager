import SessionList from "@/components/SessionList.vue";
import { createPinia, setActivePinia } from "pinia";

describe("<SessionList />", () => {
  it("contains items", () => {
    cy.intercept("GET", "/api/v0/sessions", {
      body: {
        sessions: [
          {
            id: "id123",
            description: "description abc",
            tags: [
              { name: "tag1", description: "tag description 1" },
              { name: "tag2", description: "tag description 2" },
            ],
            owner: "owner1",
            players: ["player1"],
            time: null,
          },
          {
            id: "id456",
            description: "description def",
            tags: [{ name: "tag3", description: "tag description 3" }],
            owner: "owner2",
            players: [],
            time: null,
          },
        ],
      },
    });

    cy.mount(SessionList, {
      global: {
        plugins: setActivePinia(createPinia()),
      },
    });

    cy.get(".list-group-item").should("have.length", 2);

    cy.get(".list-group-item").eq(0).find("code").should("have.text", "id123");
    cy.get(".list-group-item")
      .eq(0)
      .find(".badge")
      .should("have.length", 2)
      .should("contain.text", "tag1")
      .should("contain.text", "tag2");
    cy.get(".list-group-item")
      .eq(0)
      .find("span.text-secondary")
      .should("have.text", " by owner1");
    cy.get(".list-group-item")
      .eq(0)
      .find("div")
      .should("contain.text", "description abc");

    cy.get(".list-group-item").eq(1).find("code").should("have.text", "id456");
    cy.get(".list-group-item")
      .eq(1)
      .find(".badge")
      .should("have.length", 1)
      .should("contain.text", "tag3");
    cy.get(".list-group-item")
      .eq(1)
      .find("span.text-secondary")
      .should("have.text", " by owner2");
    cy.get(".list-group-item")
      .eq(1)
      .find("div")
      .should("contain.text", "description def");
  });
});
