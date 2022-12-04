import { IProfileInfoResponse } from "@/components/ApiService";
import { defineStore } from "pinia";

export const profileStore = defineStore("profile", {
  state: (): IProfileInfoResponse => {
    return {
      email: "",
      username: "",
      authenticated: false,
      auth_token: null,
      is_staff: false,
    };
  },
});
