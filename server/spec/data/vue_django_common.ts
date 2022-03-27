function getCookie(name: string): string | null {
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (const cookie of cookies) {
      // Does this cookie string begin with the name we want?
      if (cookie.trim().startsWith(name + "=")) {
        return decodeURIComponent(cookie.trim().substring(name.length + 1));
      }
    }
  }
  return null;
}

function getCsrfHeader(): Headers {
  const csrftoken = getCookie("csrftoken");
  const headers = new Headers();
  if (csrftoken != null) headers.append("X-CSRFToken", csrftoken);
  return headers;
}

export async function get(url: string): Promise<object> {
  return await fetch(`${process.env.VUE_APP_SERVER_URL}${url}`, {
    credentials: "include",
    headers: getCsrfHeader(),
  }).then((r) => r.json());
}

export async function post(url: string, body: object): Promise<object> {
  return await fetch(`${process.env.VUE_APP_SERVER_URL}${url}`, {
    method: "POST",
    credentials: "include",
    headers: getCsrfHeader(),
    body: JSON.stringify(body),
  }).then((r) => r.json());
}

export class SchemaValidationError implements Error {
  public constructor(public readonly message: string) {
    this.name = "SchemaValidationError";
  }

  name: string;
}
