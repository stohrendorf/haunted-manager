const EntryTypeFile = 0;

const HeaderSize = 512;
const TypeOffset = 156;
const TypeSize = 1;
const SizeOffset = 124;
const SizeSize = 12;
const NameOffset = 0;
const NameSize = 100;

function _tarRead(data: Uint8Array, offset: number, size: number): Uint8Array {
  return data.subarray(offset, offset + size);
}

export interface IEntry {
  name: string;
  size: number;
  offset: number;
}

export function getFiles(data: Uint8Array): IEntry[] {
  let offset = 0;
  const entries: IEntry[] = [];

  while (offset + HeaderSize < data.byteLength) {
    const nameData = _tarRead(data, offset + NameOffset, NameSize);
    let name = "";
    for (const c of nameData) {
      if (c === 0) {
        break;
      }
      name += String.fromCharCode(c);
    }

    if (name.length === 0) {
      break;
    }

    const size = parseInt(
      _tarRead(data, offset + SizeOffset, SizeSize).reduce(
        (prev: string, b: number) => prev + String.fromCharCode(b),
        "",
      ),
      8,
    );
    const type = parseInt(
      _tarRead(data, offset + TypeOffset, TypeSize).reduce(
        (prev: string, b: number) => prev + String.fromCharCode(b),
        "",
      ),
    );

    // Save this as en entry if it is a file or directory
    if (type === EntryTypeFile) {
      entries.push({
        name: name,
        size: size,
        offset: offset,
      });
    }

    offset += size + HeaderSize;
    if (offset % HeaderSize > 0) {
      offset = (offset / HeaderSize + 1) * HeaderSize;
    }
  }

  return entries;
}

export function getData(entry: IEntry, data: Uint8Array): Uint8Array {
  return _tarRead(data, entry.offset + HeaderSize, entry.size);
}
