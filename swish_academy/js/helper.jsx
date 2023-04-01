export default async function fetchCall(url, handleData, method = "GET") {
  fetch(url, { method, credentials: "same-origin" })
    .then((response) => {
      if (!response.ok) throw Error(response.statusText);
      return response.json();
    })
    .then(handleData)
    .catch((error) => console.log(error));
}
