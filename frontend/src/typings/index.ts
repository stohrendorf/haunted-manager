declare module "xzwasm" {
  class XzReadableStream implements ReadableStream<Uint8Array> {
    constructor(data: ReadableStream<Uint8Array>);
    readonly locked: boolean;

    cancel(reason?: any): Promise<void>;

    getReader(options: { mode: "byob" }): ReadableStreamBYOBReader;
    getReader(): ReadableStreamDefaultReader<Uint8Array>;
    getReader(
      options?: ReadableStreamGetReaderOptions,
    ): ReadableStreamReader<Uint8Array>;

    pipeThrough<T>(
      transform: ReadableWritablePair<T, Uint8Array>,
      options?: StreamPipeOptions,
    ): ReadableStream<T>;

    pipeTo(
      destination: WritableStream<Uint8Array>,
      options?: StreamPipeOptions,
    ): Promise<void>;

    tee(): [ReadableStream<Uint8Array>, ReadableStream<Uint8Array>];
  }

  export { XzReadableStream };
}
