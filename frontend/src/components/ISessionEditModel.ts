import { ISession } from "@/components/ApiService";

export interface ISessionEditModel {
  session: ISession;
  selectedTags: number[];
}
