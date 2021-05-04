// dropzone initialization stuff

let config = {
  url: "upload/",
  disablePreviews: true,
  //  thumbnail: thumbnailHandler,
  renameFile: renameFileHandler,
  //  acceptedFiles: ".jpeg,.jpg,.png,.gif,.mp4,.mkv,.webm"
};

let myDropzone1 = new Dropzone("#upload-button", config);
let myDropzone2 = new Dropzone("#upload-button-img", config);
let myDropzone3 = new Dropzone("#upload-button-text", config);

myDropzone1.on("addedfile", addedFileHandler);
myDropzone2.on("addedfile", addedFileHandler);
myDropzone3.on("addedfile", addedFileHandler);

myDropzone1.on("success", successHandler);
myDropzone2.on("success", successHandler);
myDropzone3.on("success", successHandler);

myDropzone1.on("error", errorHandler);
myDropzone2.on("error", errorHandler);
myDropzone3.on("error", errorHandler);


function thumbnailHandler(file, dataUrl) {
  console.log("thumbnailHandler");

  let img = document.createElement('img');
  img.setAttribute('src', dataUrl);
  img.classList = "w-40 h-40 object-cover";

  let div = document.createElement('div');
  div.appendChild(img);

  document.getElementById("drpzn").appendChild(div);
}


function addedFileHandler(file) {
  console.log("A file has been added: " + JSON.stringify(file, null, 4));
}


function renameFileHandler(file) {
  let name = new Date().getTime() + "_" + file.name
  console.log(name)
  //  console.log("A file has been renamed: " + JSON.stringify(file, null, 4));
  return name
}


function successHandler(file, resp) {
  console.log('success!')
  console.log(file)
  console.log(resp)

  window.location.reload(true);
}


function errorHandler(file, error, xhr) {
  console.log('error!')

  let message = 'Please try again.'

  if (typeof(error) === 'string') {
    message = error
  } else {
    message = error['msg']
  }

  let node = document.createElement('div');
  node.innerHTML = '<div class="bg-yellow-200 border-l-4 border-yellow-600 text-yellow-700 p-4" role="alert"><p class="font-bold">Upload failed</p><p>'+ message + '</p></div>'

  Toastify({
    node: node,
    duration: 5000,
    close: true,
    gravity: "top", // `top` or `bottom`
    position: "right", // `left`, `center` or `right`
    stopOnFocus: true, // Prevents dismissing of toast on hover
    backgroundColor: '#FDE68A', // bg-yellow-200 TODO: use style attribute
  }).showToast();
}

// end dropzone stuff
// ---------------------------------------------------------------------------------------

function deleteImage(imgName) {
  console.log('deleteImage ' + imgName);

  $.ajax({
    type: "POST",
    url: "/delete/",
    data: JSON.stringify({'name' : imgName}),
    success: function () {
      console.log('success');

      function reload() {
        window.location.reload(true);
      }

      setTimeout(reload, 500);
    },
    error: function () {
      console.log('error');
    },
    dataType: 'json',
    contentType: 'application/json',
  });

  //  console.log(event.srcElement.id)
}


// preload images in gallery
$.get('/all', null, function(data) {
  data.reverse().forEach( function(url) {
    console.log(url);

    let img = document.createElement('img');
    img.setAttribute('src', url);
    img.classList = "w-40 h-40 object-cover";

    let deleteButton = document.createElement('div')
    deleteButton.id =
      deleteButton.classList = "w-10 h-10 bg-red-500 hover:bg-red-600 text-red-100 cursor-pointer absolute top-0 right-0 flex justify-center items-center"
    deleteButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" /></svg>'


    let imgNameParts = url.split('/')
    let imgName = imgNameParts[imgNameParts.length - 1]

    deleteButton.onclick = function() {
      deleteImage(imgName);
    }

    let div = document.createElement('div');
    div.classList = "transform hover:scale-105 relative";
    //div.classList = "relative group";

    div.appendChild(deleteButton);
    div.appendChild(img);

    document.getElementById("drpzn").appendChild(div)
  })
});
