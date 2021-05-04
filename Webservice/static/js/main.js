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

// ---------------------------------------------------------------------------------------

// preload images in gallery
$.get('/all', null, function(data) {
  data.reverse().forEach( function(url) {

    let img = document.createElement('img');
    img.setAttribute('src', url);
    img.classList = "w-40 h-40 object-cover";

    let div = document.createElement('div');
    div.appendChild(img);
    document.getElementById("drpzn").appendChild(div)
  })
});
