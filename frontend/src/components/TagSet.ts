import { ITag } from "@/components/ApiService";

export default class TagSet {
  constructor(tags: ITag[] = []) {
    const tmp = new Map<number, ITag>();
    for (const tag of tags) {
      tmp.set(tag.id, tag);
    }

    this.tags = [...tmp.values()];
    this.tags.sort((a, b) => a.name.localeCompare(b.name));
  }

  public tags: ITag[];
}
