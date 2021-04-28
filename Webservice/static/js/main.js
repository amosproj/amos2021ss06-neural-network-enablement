// dropzone initialization stuff

let config = {
  url: "upload/",
  disablePreviews: true,
  thumbnail: thumbnailHandler,
  renameFile: renameFileHandler,
  acceptedFiles: ".jpeg,.jpg,.png,.gif,.mp4,.mkv,.webm"
};

let myDropzone1 = new Dropzone("#upload-button", config);
let myDropzone2 = new Dropzone("#upload-button-img", config);
let myDropzone3 = new Dropzone("#upload-button-text", config);

myDropzone1.on("addedfile", addedFileHandler);
myDropzone2.on("addedfile", addedFileHandler);
myDropzone3.on("addedfile", addedFileHandler);


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