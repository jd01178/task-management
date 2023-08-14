const drag = (event) => {
  event.dataTransfer.setData("text/plain", event.target.id);
}

const allowDrop = (ev) => {
  ev.preventDefault();
  if (hasClass(ev.target, "dropzone")) {
    addClass(ev.target, "droppable");
  }
}

const clearDrop = (ev) => {
  removeClass(ev.target, "droppable");
}

const drop = (event) => {
  event.preventDefault();
  const data = event.dataTransfer.getData("text/plain");
  const element = document.querySelector(`#${data}`);
  try {
    // Check if the dropzone contains the spacer content
    if (hasClass(event.target, "dropzone")) {
      // Remove the spacer content from dropzone
      $(event.target).empty();
    }

    // Add the draggable content
    event.target.appendChild(element);

    // Get the task ID from the dropped element
    const taskId = element.id;

    // Get the status from the drop zone's ID
    const newStatus = event.target.id;

    // Send an HTTP request to update the task status on the backend
    updateTaskStatus(taskId, newStatus)
      .then(() => {
        updateDropzones();
        location.replace(location.href);
      })
      .catch((error) => {
        console.error(error);
        console.warn("Can't move the item to the same place");
      });
  } catch (error) {
    console.error(error);
    console.warn("Can't move the item to the same place");
  }
};

const updateDropzones = () => {
    /* after dropping, refresh the drop target areas
      so there is a dropzone after each item
      using jQuery here for simplicity */

    var dz = $('<div class="dropzone" ondrop="drop(event)" ondragover="allowDrop(event)" ondragleave="clearDrop(event)"> &nbsp; </div>');

    // delete old dropzones
    $('.dropzone').remove();

    // insert new dropdzone after each item
    dz.insertAfter('.card.draggable');

    // insert new dropzone in any empty swimlanes
    $(".items:not(:has(.card.draggable))").append(dz);
};


const updateTaskStatus = async (taskId, newStatus) => {
  // remove the "task-" prefix from the task ID
  taskId = taskId.replace("task-", "");
  console.log(taskId, newStatus);
  const url = `/api/v1/task-progress/${taskId}/`;

  try {
    const response = await sendPatchRequest(url, { progress: newStatus });

    if (!response.ok) {
      throw new Error("Failed to update task status on the backend.");
    }

    // Task status updated successfully
    return await response.json();
  } catch (error) {
    console.error(error);
    throw error;
  }
};

// helpers (unchanged)...


// helpers
function hasClass(target, className) {
    return new RegExp('(\\s|^)' + className + '(\\s|$)').test(target.className);
}

function addClass(ele,cls) {
  if (!hasClass(ele,cls)) ele.className += " "+cls;
}

function removeClass(ele,cls) {
  if (hasClass(ele,cls)) {
    var reg = new RegExp('(\\s|^)'+cls+'(\\s|$)');
    ele.className=ele.className.replace(reg,' ');
  }
}

function unwrap(node) {
    node.replaceWith(...node.childNodes);
}

