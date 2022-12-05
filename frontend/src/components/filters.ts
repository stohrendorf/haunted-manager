import "moment-timezone";
import moment from "moment/moment";

export function datetime(value: string): string {
  return moment(value)
    .tz(moment.tz.guess())
    .locale(navigator.language)
    .format("LLLL");
}

export function seconds(value: number): string {
  return moment
    .utc(moment.duration(value, "seconds").asMilliseconds())
    .format("HH:mm:ss");
}

export function prettyBytes(bytes: number, kib: boolean = false): string {
  if (bytes === 0) {
    return "0 Bytes";
  }
  const base = kib ? 1024 : 1000;
  const sizes = kib ? ["Bytes", "KiB", "MiB"] : ["Bytes", "KB", "MB"];
  const exp = Math.floor(Math.log(bytes) / Math.log(base));
  return (bytes / Math.pow(base, exp)).toFixed(1) + " " + sizes[exp];
}
