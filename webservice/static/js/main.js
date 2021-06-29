// helpers

function showWarningToast(headline, message) {
  let node = document.createElement('div');
  node.innerHTML = document.querySelector('#template-toast-warn').innerHTML;

  node.querySelector('#toast-headline').textContent = headline;
  node.querySelector('#toast-message').textContent = message;

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


// -------------------------------------------------------------------------

// dropzone initialization stuff

let config = {
  url: "/upload/",
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

// success handler: called, after dropzone library successfully uploaded a file
function successHandler(file, resp) {
  console.log('success!')
  //console.log(file)
  //console.log(resp)

  window.location.reload(true);
}


// error handler: called, after dropzone library fails to upload a file
function errorHandler(file, error, xhr) {
  console.log('error!')

  let message = 'Please try again.'

  if (typeof(error) === 'string') {

    if (error === 'Server responded with 0 code.') {
      // Improve default error message by dropzone
      message = "Couldn't connect to localhost, is the webservice still running?"
    } else {
      message = error;
    }

  } else {
    // print response by api
    message = error['msg']

    showWarningToast('File upload failed', message);
  }
}

// end dropzone stuff
// ---------------------------------------------------------------------------------------


// sends the service a request to delete the image
// after the user clicked on the 'delete icon'
function deleteImage(imgName) {
  console.log('deleteImage ' + imgName);

  $.ajax({
    type: "POST",
    url: "/delete/",
    data: JSON.stringify({
      'name': imgName
    }),
    success: function() {
      console.log('success');

      function reload() {
        window.location.reload(true);
      }

      setTimeout(reload, 500);
    },
    error: function() {
      showWarningToast("Deleting image failed.", "Couldn't connect to server. Is the service running?");
    },
    dataType: 'json',
    contentType: 'application/json',
  });
}


// sends the service a request to colorize the image
// after the user clicked on the 'colorize icon',
// if successful it calls the showResult function
function colorizeImageAndShowResult(imgName) {
  console.log(imgName, 'colorize')

  // call colorize function
  $.ajax({
    type: "POST",
    url: "/colorize/",
    data: JSON.stringify({
      'name': imgName
    }),
    success: function(response) {
      console.log(response['msg']);
      showResult(imgName);
    },
    error: function(error) {
      if (error.status === 500 || error.status === 400) {
        let msg = error['responseJSON']['msg'];
        showWarningToast("Colorizing image failed.", msg);
        console.log(msg)
      } else {
        showWarningToast("Colorizing image failed.", "The error was logged to the console.")
        console.log('Colorizing image failed.', error)
      }
    },
    dataType: 'json',
    contentType: 'application/json',
  });
}


// displays the original and the colorized image next to each other
function showResult(imgName) {
  console.log('showResult', imgName);

  // TODO: This should really be a GET request
  $.ajax({
    type: "POST",
    url: "/result/",
    data: JSON.stringify({
      'name': imgName
    }),
    success: function(response) {
      let original = response['origin'];
      let colorized = response['colorized'];

      if (original.includes(imgName)) {
        console.log(colorized);

        // show result page popup
        document.querySelector('#result-image-original').setAttribute('src', original);
        document.querySelector('#result-image-colorized').setAttribute('src', colorized);

        setTimeout(function() {
          document.querySelector('#result-colorize').classList.remove('invisible');
        }, 100);
      }
    },
    error: function(error) {
      console.log(error);
      showWarningToast("Loading the result failed.", "Couldn't connect to server. Is the service running?");
    },
    dataType: 'json',
    contentType: 'application/json',
  });
}


// ---------------------------------------------------------------------------------------
// This is called on every page load.
//
// load images and display them in gallery
$.get('/all/', null, function(data) {
  if (data.length > 0) {
    document.getElementById('drpzn').classList.remove('invisible');

    data.sort(function(a, b) {
      return a.thumbnail.localeCompare(b.thumbnail);
    });

    data.forEach(function(data) {
      let url = data.thumbnail
      let type = data.type

      let div = document.createElement('div');
      div.innerHTML = document.querySelector('#template-gallery-image').innerHTML
      console.log(div)

      div.querySelector('#gallery-image').setAttribute('src', url);

      if (type === 'video') {
        div.querySelector('#video-icon').classList.remove('invisible');
      }

      let imgNameParts = url.split('/')
      let imgName = imgNameParts[imgNameParts.length - 1]

      let imgButton = div.querySelector('#delete-image-button');

      imgButton.onclick = function() {
        // only allow one mouseclick, remove the eventlistener after first click
        imgButton.onclick = function() {}

        deleteImage(imgName);
      }

      let colorizeButton = div.querySelector('#colorize-image-button');
      colorizeButton.onclick = function() {
        colorizeImageAndShowResult(imgName);
      }

      document.getElementById("drpzn").appendChild(div)
    })
  }
});
