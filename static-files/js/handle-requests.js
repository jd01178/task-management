function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');
const sendPostRequest = async (url, data) => {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify(data),
  });
  return response.json();
};

const sendGetRequest = async (url) => {
  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
  });
  return response.json();
};

const sendPutRequest = async (url, data) => {
  const response = await fetch(url, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify(data),
  });
  return response.json();
};

const sendPatchRequest = async (url, data) => {
  const response = await fetch(url, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify(data),
  });
  return response.json();
};

const sendDeleteRequest = async (url) => {
  const response = await fetch(url, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
  });
  return response.json();
};

const sendPostRequestWithFile = async (url, data) => {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: data,
  });
  return response.json();
};

const sendPutRequestWithFile = async (url, data) => {
  const response = await fetch(url, {
    method: 'PUT',
    headers: {
      'X-CSRFToken': csrftoken,
    },
    body: data,
  });
  return response.json();
};

const sendPatchRequestWithFile = async (url, data) => {
  const response = await fetch(url, {
    method: 'PATCH',
    headers: {
      'X-CSRFToken': csrftoken,
    },
    body: data,
  });
  return response.json();
};

