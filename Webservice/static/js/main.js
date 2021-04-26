//console.log('test');
/*
$(document).ready(function(){
    $('#upload-button').on('click',function(){
        alert("JQuery Running!");
    });
}); */


let config = {
  url: "upload/",
  disablePreviews: true,
  thumbnail: thumbnailHandler,
};

let myDropzone1 = new Dropzone("#upload-button", config);
let myDropzone2 = new Dropzone("#upload-button-img", config);

myDropzone1.on("addedfile", addedFileHandler);
myDropzone2.on("addedfile", addedFileHandler);


function thumbnailHandler(file, dataUrl) {
  let img = document.createElement('img');
  img.setAttribute('src', dataUrl);
  img.classList = "w-40 h-40 object-cover";

  let div = document.createElement('div');
  div.appendChild(img);

  let before = document.getElementById("upload-button");
  document.getElementById("drpzn").insertBefore(div, before);
}

function addedFileHandler(file) {
// console.log("A file has been added: " + JSON.stringify(file, null, 4));
}

