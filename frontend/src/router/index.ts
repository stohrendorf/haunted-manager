import CreateSession from "@/components/CreateSession.vue";
import EditGhost from "@/components/EditGhost.vue";
import EditSession from "@/components/EditSession.vue";
import GhostList from "@/components/GhostList.vue";
import ProfileView from "@/components/ProfileView.vue";
import RegisterAccount from "@/components/RegisterAccount.vue";
import SessionList from "@/components/SessionList.vue";
import UploadGhost from "@/components/UploadGhost.vue";
import { createRouter, createWebHashHistory } from "vue-router";

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: "/", component: SessionList },
    { path: "/create-session", component: CreateSession },
    { path: "/edit-session/:id", component: EditSession },
    { path: "/profile", component: ProfileView },
    { path: "/register", component: RegisterAccount },
    { path: "/ghosts", component: GhostList },
    { path: "/upload-ghosts", component: UploadGhost },
    { path: "/edit-ghost/:id", component: EditGhost },
  ],
  linkActiveClass: "active",
});

export default router;
