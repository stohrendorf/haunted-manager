import { createRouter, createWebHashHistory } from "vue-router";
import ProfileView from "@/components/ProfileView.vue";
import RegisterAccount from "@/components/RegisterAccount.vue";
import SessionList from "@/components/SessionList.vue";
import CreateSession from "@/components/CreateSession.vue";
import EditSession from "@/components/EditSession.vue";

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: "/", component: SessionList },
    { path: "/create-session", component: CreateSession },
    { path: "/profile", component: ProfileView },
    { path: "/register", component: RegisterAccount },
    { path: "/edit-session/:id", component: EditSession },
  ],
  linkActiveClass: "active",
});

export default router;
