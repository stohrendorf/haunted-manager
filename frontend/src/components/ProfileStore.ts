import { defineStore } from "pinia";
import { IProfileInfoResponse } from "@/components/ApiService";

export const profileStore = defineStore("profile", {
  state: (): IProfileInfoResponse => {
    return {
      email: "",
      username: "",
      authenticated: false,
      verified: false,
      auth_token: null,
    };
  },
});
