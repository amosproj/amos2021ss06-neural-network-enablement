// dropzone initialization stuff

let config = {
  url: "upload/",
  disablePreviews: true,
  //  acceptedFiles: ".jpeg,.jpg,.png,.gif,.mp4,.mkv,.webm"
};

let myDropzone1 = new Dropzone("#upload-button", config);
let myDropzone2 = new Dropzone("#upload-button-img", config);
let myDropzone3 = new Dropzone("#upload-button-text", config);

myDropzone1.on("success", successHandler);
myDropzone2.on("success", successHandler);
myDropzone3.on("success", successHandler);

myDropzone1.on("error", errorHandler);
myDropzone2.on("error", errorHandler);
myDropzone3.on("error", errorHandler);


function successHandler(file, resp) {
  console.log('success!')
  //console.log(file)
  //console.log(resp)

  window.location.reload(true);
}


function errorHandler(file, error, xhr) {
  console.log('error!')

  let message = 'Please try again.'

  if (typeof(error) === 'string') {

    if (error === 'Server responded with 0 code.') {
      // Improve default error message by dropzone
      message = "Couldn't connect to localhost, is the backend running?"
    } else {
      message = error;
    }

  } else {
    // print response by api
    message = error['msg']
  }

  var node = document.createElement('div');
  node.innerHTML = document.querySelector('#template-toast-warn').innerHTML

  node.querySelector('#toast-headline').textContent = 'File upload failed.';
  node.querySelector('#toast-message').textContent = message

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


// callback function that sends the service a request to delete the image
// when the user clicked on the 'delete icon'
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


// load images in gallery
$.get('/all', null, function(data) {
  data.reverse().forEach( function(url) {
    console.log(url);

    var div = document.createElement('div');
    div.innerHTML = document.querySelector('#template-gallery-image').innerHTML
    console.log(div)

    div.querySelector('#gallery-image').setAttribute('src', url);

    let imgNameParts = url.split('/')
    let imgName = imgNameParts[imgNameParts.length - 1]

    div.querySelector('#delete-image-button').onclick = function() {
      deleteImage(imgName);
    }

    document.getElementById("drpzn").appendChild(div)
  })
});
