import { ISessionsResponse, ITagsResponse } from "@/components/ApiService";
import SessionList from "@/components/SessionList.vue";
import { createPinia, setActivePinia } from "pinia";

describe("<SessionList />", () => {
  beforeEach(() => {
    cy.intercept("GET", "/api/v0/tags", {
      body: {
        tags: [],
      } as ITagsResponse,
    });
  });

  it("contains items", () => {
    cy.intercept("GET", "/api/v0/sessions", {
      body: {
        sessions: [
          {
            id: "id123",
            description: "description abc",
            tags: [
              { id: 1, name: "tag1", description: "tag description 1" },
              { id: 2, name: "tag2", description: "tag description 2" },
            ],
            owner: "owner1",
            players: ["player1"],
            time: null,
            private: true,
          },
          {
            id: "id456",
            description: "description def",
            tags: [{ id: 3, name: "tag3", description: "tag description 3" }],
            owner: "owner2",
            players: [],
            time: null,
            private: false,
          },
        ],
      } as ISessionsResponse,
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

  it("shows and hides private indicator", () => {
    cy.intercept("GET", "/api/v0/sessions", {
      body: {
        sessions: [
          {
            id: "id123",
            description: "description abc",
            tags: [
              { id: 1, name: "tag1", description: "tag description 1" },
              { id: 2, name: "tag2", description: "tag description 2" },
            ],
            owner: "owner1",
            players: ["player1"],
            time: null,
            private: true,
          },
          {
            id: "id456",
            description: "description def",
            tags: [{ id: 3, name: "tag3", description: "tag description 3" }],
            owner: "owner2",
            players: [],
            time: null,
            private: false,
          },
        ],
      } as ISessionsResponse,
    });

    cy.mount(SessionList, {
      global: {
        plugins: setActivePinia(createPinia()),
      },
    });

    cy.get(".list-group-item").should("have.length", 2);

    cy.get(".list-group-item")
      .eq(0)
      .find(".bi.bi-eye-slash")
      .should("be.visible");
    cy.get(".list-group-item")
      .eq(1)
      .find(".bi.bi-eye-slash")
      .should("not.exist");
  });

  it("shows and hides edit and delete buttons", () => {
    const privilegedUsername = "owner";
    cy.intercept("GET", "/api/v0/sessions", {
      body: {
        sessions: [
          {
            id: "id123",
            description: "description abc",
            tags: [
              { id: 1, name: "tag1", description: "tag description 1" },
              { id: 2, name: "tag2", description: "tag description 2" },
            ],
            owner: privilegedUsername,
            players: ["player1"],
            time: null,
            private: false,
          },
          {
            id: "id456",
            description: "description def",
            tags: [{ id: 3, name: "tag3", description: "tag description 3" }],
            owner: privilegedUsername + "-unprivileged",
            players: [],
            time: null,
            private: false,
          },
        ],
      } as ISessionsResponse,
    });

    cy.mount(SessionList, {
      global: {
        plugins: setActivePinia(createPinia()),
      },
    }).then((wrapper) => {
      wrapper.component.profile.username = privilegedUsername;
    });

    cy.get(".list-group-item").should("have.length", 2);

    cy.get(".list-group-item")
      .eq(0)
      .find(".bi.bi-trash")
      .should("exist")
      .parent()
      .should("contain.text", "Delete");
    cy.get(".list-group-item")
      .eq(0)
      .find(".bi.bi-pencil")
      .should("exist")
      .parent()
      .should("contain.text", "Edit");
    cy.get(".list-group-item").eq(1).find(".bi.bi-trash").should("not.exist");
    cy.get(".list-group-item").eq(1).find(".bi.bi-pencil").should("not.exist");
  });
});
